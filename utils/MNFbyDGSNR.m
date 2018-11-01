function  [Y, YVecs, Cn, Cx, ReconX, W, L] = MNFbyDGSNR(X, Parameters, varargin)
%function [Y, YVecs, Cn, Cx, ReconX, W, L] = MNFbyDGSNR(X, Parameters, varargin)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% FUNCTION TO COMPUTE AN MNF TRANSFORM OF THE HYPERSPECTRAL IMAGE X
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% INPUTS:
%%%     X: NRows x NCols X B Spectral Data Cube
%%%         where
%%%         B = Number of Bands
%%%         N = NRows x NCols = Number of Spectra
%%%     Parameters COMES FROM THE FILE MNFbyDGParameters.m
%%%         SEE THAT FILE FOR PARAMETER DESCRIPTIONS
%%%     varargin:
%%%         PIXEL MASK TO REMOVE SOME PIXELS FROM PARTICIPATING IN
%%%         TRANSFORM DESIGN
%%%         DOES NOT WORK RIGHT NOW SO DON'T PASS IN A PIXEL MASK
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% OUTPUTS:
%%%     Y:      NRows x NCols x NComps REDUCED DIM SPECTRAL DATA CUBE
%%%     YVecs:  NRows*NCols x NComps REDUCED DIM SPECTRA VECTOR ARRAY
%%%     Cn:     ESTIMATED COVARIANCE OF NOISE
%%%     ReconX: Reconstruction of X from Y
%%%     W:      MNF TRANSFORM MATRIX
%%%                 IF ZEROMEAN IS false, THEN
%%%                     XVecs IS NRows*NCols x B VECTOR ARRAY
%%%                         FORMED BY RESHAPING X
%%%                 ELSE
%%%                     XVecs IS NRows*NCols x B VECTOR ARRAY
%%%                         FORMED BY RESHAPING X-(SPECTRAL MEAN OF X)
%%%                 END
%%%                 THE TRANSFORM IS YVecs = W*XVecs(:, 1:NComps);
%%%     L:      EIGENVALUES OF inv(Cn)Cx
%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% AUTHOR: Darth Gader %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
%%% SET PARAMETER VARIABLES. SEE THE FILE MNFbyDGParameters.m  %%%
NComps    = Parameters.NComps;
NoiseMask = Parameters.NoiseMask;
Method    = Parameters.Method;
ZEROMEAN  = Parameters.ZEROMEAN;
DIAGLOAD  = Parameters.DIAGLOAD;

%%
%%% INITIALIZE SIZES %%%
Sx    = size(X);

if(length(Sx) == 3)
    NRows = Sx(1);
    NCols = Sx(2);
    N = Sx(1)*Sx(2);
    B = Sx(3);
else
    error('Number of dimensions of X is not 3');
end

if(length(varargin)> 0)
    PixelMask = varargin{1};
    PixelMask = reshape(PixelMask, [NRows*NCols, 1]);
    PixelMask = repmat(PixelMask, [1, B]);
else
    PixelMask = false;
end
%%
%%% CALCULATE  NOISE COVARIANCE %%%
SubNbrs = zeros(size(X));
for b = 1:B;
    XSlice           = squeeze(X(:, :, b));
    SubNbrs(:, :, b) = conv2(XSlice, NoiseMask, 'same');
end
SubNbrs = reshape(SubNbrs, [N, B]);
Cn      = cov(SubNbrs);

fprintf('\nCondition Number of Cn Before Diagonal Load= %f\n', cond(Cn));
if(DIAGLOAD)
    Cn = Cn +eye(size(Cn)).*(DIAGLOAD*max(Cn(:)));
end
fprintf('Condition Number of Cn  After Diagonal Load= %f\n', cond(Cn));

%%
%%% CALCULATE OBSERVATION COVARIANCE %%%
XVecs = reshape(X, [N, B]);
Cx     = cov(XVecs);
fprintf('\nCondition Number of Cx Before Diagonal Load= %f\n', cond(Cx));
if(DIAGLOAD>eps)
    Cx = Cn +eye(size(Cx)).*(DIAGLOAD*max(Cx(:)));
end
fprintf('Condition Number of Cx After  Diagonal Load= %f\n', cond(Cx));

%%
%%% CALCULATE LEFT EIGENVECTOR & EIGENVALUES OF Cn,inv*C %%%
if(Parameters.SNR)
    if(strcmp(Method, 'ConstructEig'))
        [U, Lambda]   = svd(Cn);
        U             = U';
        InvSqRtLambda = pinv(sqrt(Lambda));
        Cnx           = InvSqRtLambda*U*Cx*U'*InvSqRtLambda;
        [V,Dnx]       = svd(Cnx);
        V             = V';
        W             = U'*InvSqRtLambda*V';
        L             = diag(Dnx);
    elseif(strcmp(Method, 'DirectEig'))
        [V,D,W] = svd(inv(Cn)*Cx);
        L       = diag(D);
    else
        error('Unknown Eigen Computation Method');
    end
else
    if(strcmp(Method, 'ConstructEig'))
        [U, Lambda]   = svd(Cx);
        U             = U';
        InvSqRtLambda = pinv(sqrt(Lambda));
        Cxn           = InvSqRtLambda*U*Cn*U'*InvSqRtLambda;
        [V,Dxn]       = svd(Cxn);
        V             = V';
        W             = U'*InvSqRtLambda*V';
        L             = diag(Dxn);
    elseif(strcmp(Method, 'DirectEig'))
        [V,D,W] = svd(inv(Cx)*Cn);
        L       = diag(D);
    else
        error('Unknown Eigen Computation Method');
    end
end

%%
%%% SUBTRACT MEAN %%%
if(ZEROMEAN)
    Xmu    = mean(XVecs);
    XmuBig = repmat(Xmu, [N, 1]);
    XVecs  = XVecs - XmuBig;
end
%%
%%% CALCULATE TRANSFORM (Tx) %%%
%%% ROWS OF W' ARE LEFT EIGENVECTORS OF R = Cn*pinv(Cx)
%%% COMPUTING W'* R = (R'*W)' SO WE COMPUTE Xvecs*W;

%%% COLUMNS OF W ARE THE RIGHT EIGENVECTORS OF inv(Cn)*Dx %%%
%%% TRANSPOSE TO MATCH NOTATION IN NOTES. IF SPEED REQ., UNDO TRANSPOSES %%%
%%% OF XVecs AND YVecs (this is down a couple of blocks of code) %%%
XVecs = XVecs';
YVecs = W(:, (end-NComps+1:end))'*XVecs;

%%%XXX DEBUGGING XXX%%%
TxNoiseVecs = W(:, (end-NComps+1):end)'*SubNbrs';

%%% RECONSTRUCT ORIGINAL IMAGE  AND CALCULATE ERROR STATISTICS %%%
InvTx  = inv(W');
ReconX = InvTx(:, (end-NComps+1:end))*YVecs;
Err    = ReconX-XVecs;
RMSE   = sqrt(mean(Err(:).*Err(:)));
fprintf('\nRMS Error = %8.4f\n', RMSE);

%%% PLOT HISTOGRAM OF ERRORS IF DESIRED %%%
if(Parameters.PlotHist)
    MinErr = min(Err(:));
    MaxErr = max(Err(:));
    StpSz  = (MaxErr-MinErr)/20;
    Domain = MinErr:StpSz:MaxErr;
    figure(13579);hist(Err(:), Domain);title('Reconstruction Error Histogram')
end


%%
%%% NOW THAT TRANSFORMS COMPLETE, TRANSFORM YVecs BACK TO IMAGE %%%
%%% AGAIN, IF SPEED/MEMORY PROBLEMS, UNDO THE TRANSPOSES HERE & ABOVE   %%%
YVecs  = YVecs';
YVecs = fliplr(YVecs); %%% for plotting
ReconX = ReconX';

%%% TURN Y AND ReconX BACK INTO AN IMAGES %%%
Y      = reshape(YVecs,  [NRows, NCols,NComps]);
ReconX = reshape(ReconX, [NRows, NCols,B]);
return
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% END OF FUNCTION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




%%% OLD DEBUGGING CODE XXX %%%
% keyboard
% s = 1;
% meanX = mean(X,3)
% for e = 3:10:103;
%     RBeg = InvTx(:, s:e)*YVecs(s:e, :);
%     REnd = InvTx(:, end-e+1:end)*YVecs(end-e+1:end, :);
%     ImBeg = reshape(RBeg', [NRows, NCols, B]);
%     ImEnd = reshape(REnd', [NRows, NCols, B]);
%     figure(400);
%     imagesc(mean(ImBeg, 3), [0, 0.6]); colorbar;
%     figure(401);
%     imagesc(mean(ImEnd,3), [0, 0.6]); colorbar;
%     figure(403)
%     imagesc(meanX, [0, 0.6]); colorbar'
%     figure(404)
%     imagesc(abs(meanX - mean(ImBeg, 3)), [0, 0.6]); colorbar
%     figure(405)
%     imagesc(abs(meanX - mean(ImEnd, 3)),[0, 0.6]); colorbar
%     pause;
%
% end

