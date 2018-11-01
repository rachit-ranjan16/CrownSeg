 function [Clusts,ClustsFlag,ClustMems, ClustVecs,KLDMat,Hists] = HierarchClusterByDGVer2(X, Wvs,Parameters);
%function [Clusts,ClustFlag,ClustMems, ClustVecs,KLDMat,Hists] = HierarchClusterByDGVer2(X, Wvs, Parameters);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%% A FUNCTION TO DEMONSTRATE HIERARCHICAL CLUSTERING
%%% AUTHOR: Darth Gader 071818
%%% LINK:   XXX
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%% INPUTS:
%%%   X: R x C x B or N=R*C x B ARRAY OF B-DIM DATA
%%%   Wvs: B-DIM VECTOR OF WAVELENGTHS
%%%   Parameters: FROM HierarchClusterByDGParameters
%
%%% OUTPUTS:
%%%   Clusts: AN ARRAY OF STRUCTURES
%%%           EACH STRUCTURE REPRESENTS A CLUST
%%%           AND HAS FIELDS
%%%              Idx: ARRAY OF INDICES OF WAVELENGTHS IN EACH CLUSTER
%%%              Wvs: ARRAY OF WAVELENGTHS IN EACH CLUSTER
%%%              IntClustD:  SMALLEST
%%%   DistMat: B X B ARRAY OF PAIRWISE SYMMETRIC KL-DIVERGENCES
%%%            THE LOWER TRIANGULAR PART IS REDUNDANT
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
%%% INITIALIZE PARAMETERS AND SIZES %%%
Nc         = Parameters.Nc;
NBins      = Parameters.NBins;
Verbose    = Parameters.Verbose;
SmScFac    = Parameters.SmScFac;

%%% ERROR CHECKING: MAKE SURE X IS N x B %%%
NIndsX = length(size(X));
switch NIndsX
    case 3
        N = size(X,1)*size(X,2);
        B = size(X,3);
        X = reshape(X, [N, B]);
    case 2
        N = size(X,1);
        B = size(X,2);
    otherwise
        error('X must be a 2 or 3 dim array');
end

%%
%%% CALCULATE KL-DIVEGENCES, HISTOGRAMS, AND UpperBd WHICH IS A    %%%
%%% NUMBER TWICE AS LARGE AS THE LARGEST KL-DIVERGENCE AND USE TO  %%%
%%%
%%% MORE PRECISELY:
%%% KLDMAT IS A MATRIX THAT
%%%    STORES SYMMETRIC KL-Divergences BETWEEN ALL BANDS IN UPPER TRIANGLE %%%
%%%    THE DIAGONAL AND LOWER TRIANGLE ALL HAVE VALUES UpperBd.            %%%
[KLDMat, Hists, UpperBd]  = computeKLDivergencesBetweenBands(X,Wvs,Parameters);

%%% INITIALIZE CLUSTERS SUCH THAT EACH CLUSTER IS ONE BAND %%%
for ck = 1:B
    Clusts(ck).Idx       = [ck];
    Clusts(ck).Wvs       = [Wvs(ck)];
    Clusts(ck).IntClustD = UpperBd;
    Clusts(ck).Rep       = ck;
    Clusts(ck).RepWv     = Wvs(ck);
end
%%% INITIALIZE ARRAY OF FLAGS INDICATING INDICES OF CLUSTERS %%%
ClustsFlag = true(B, 1);

%%

%%% TAKE CARE OF SPECIAL CASE THAT Nc= B %%%
if (Nc & (Nc < B))
    %%
    
    %%% RepDMat IS A MATRIX THAT STORES DISTANCES BETWEEN CLUSTER REPS.      %%%
    %%%    USED TO DECIDE WHICH CLUSTERS TO MERGE.                           %%%
    %%%    MODIFIED EVERY ITER TO REMOVE CLUSTERS MERGED INTO OTHER CLUSTERS %%%
    RepDMat          = KLDMat;
    
    %%% SymKLDMat IS A SYMMETRIC MATRIX THAT STORES THE KL-Div BETWEEN %%%
    %%% BANDS r AND c IN SymKLDMat(r,c) AND SymKLDMat(c,r).            %%%
    SymKLDMat        = triu(KLDMat)+triu(KLDMat)'-2*eye(B)*KLDMat(1,1);
    
    %%
    %%% MERGE CLUSTERS UNTIL                               %%%
    %%% CURRENT NUM CLUSTS == DESIRED NUM CLUSTS (K == Nc) %%%
    %%% ONE MERGE PER PASS THRU THE LOOP                   %%%
    Iter  = 0;
    while ((sum(ClustsFlag) > Nc) & (Iter < Parameters.MaxIters))
        Iter = Iter+1;
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%% SPECIAL CASE OF MERGING LAST TWO WHEN Nc == 1 %%%
        if ( (Nc == 1) & (sum(ClustsFlag) == 2))
            [Clusts, ClustsFlag] = MergeLastTwo(Clusts, ClustsFlag, SymKLDMat, Wvs, B);
        else
            %%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%% CASE: MORE THAN ONE CLUSTER IS DESIRED, Nc > 1            %%%
            %%%       AND
            %%%       HAVEN'T FOUND Nc CLUSTERS YET, sum(ClustFlag) > Nc  %%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            %%% FIND MIN KL-DIVERGENCE BETWEEN CLUSTER REPS %%%
            %%% R DENOTES ROW, C DENOTES COLUMN             %%%
            [MinREachC, MinRIdxEachC] = min(RepDMat);
            [MinAll, MinC]            = min(MinREachC);
            MinR                      = MinRIdxEachC(MinC);
            Rep1Idx                   = MinR;
            Rep2Idx                   = MinC;
            
            %%% PARTIALLY MERGE OLD CLUSTS INTO NewClust %%%
            %%% SET Idx AND Wvs OF NewClust TO UNIONS OF %%%
            %%% Clust1.Idx & Clust2.Idx AND              %%%
            %%% Clust1.Wvs & Clust2.Wvs                  %%%
            Clust1       = Clusts(Rep1Idx);
            Clust2       = Clusts(Rep2Idx);
            NewClust.Idx = union(Clust1.Idx, Clust2.Idx);
            NewClust.Wvs = Wvs(NewClust.Idx);
            
            %%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%% CASE: EACH CLUSTER HAS ONE MEMBER.           %%%
            %%%       USE Rep = Rep1Idx SINCE THERE IS ONLY  %%%
            %%%       ONE INTER-CLUST DISTANCE               %%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            if(length(NewClust.Idx) == 2)
                
                %%% UPDATE NEW CLUSTER AND STORE AT INDEX Rep1Idx %%%
                NewClust.Rep        = Rep1Idx;
                NewClust.RepWv      = Wvs(Rep1Idx);
                NewClust.IntClustD  = SymKLDMat(Rep1Idx, Rep2Idx);
                Clusts(Rep1Idx)     = NewClust;
                ClustsFlag(Rep1Idx) = true;
                Rep                 = Rep1Idx;
                
                %%% REMOVE NON-CLUSTER %%%
                Clusts(Rep2Idx).Idx = [];
                ClustsFlag(Rep2Idx)  = false;
                RepDMat(:, Rep2Idx) = UpperBd;
                RepDMat(Rep2Idx, :) = UpperBd;
                
            else
                %%
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                %%% MERGE WHEN AT LEAST ONE CLUSTER HAS > ONE MEMBER  %%%
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                %%% GET MATRIX OF DISTANCES BETWEEN ALL CLUST MEMBERS %%%
                LitDMat            = SymKLDMat(NewClust.Idx, NewClust.Idx);
                NMems              = size(LitDMat, 1);
                assert(NMems>2, 'There are supposed to be more than 2 members in this cluster');
                
                %%% CALCULATE AVE DISTS FROM EACH MEMBER TO ALL OTHERS %%%
                AllIntClustDs      = sum(LitDMat)/(NMems-1);
                
                %%% SET Rep TO INDEX OF MEMBER WITH MIN AVE DIST TO ALL MEMBERS %%%
                [IntClustD, Rep]   = min(AllIntClustDs);
                ClustMems          = NewClust.Idx;
                Rep                = ClustMems(Rep);
                
                %%% UPDATE NEW CLUST %%%
                NewClust.Rep       = Rep;
                NewClust.RepWv     = Wvs(Rep);
                NewClust.IntClustD = IntClustD;
                Clusts(Rep)        = NewClust;
                %%
                %%% NOW THAT NEW CLUSTER HAS BEEN FORMED              %%%
                %%% FINALIZE IT'S PROPERTIES, FIND INDEX TO STORE IT  %%%
                %%% AND REMOVE OTHER CLUSTER OR CLUSTERS              %%%
                
                %%% STORE NEW CLUSTER AT INDEX Rep %%%
                ClustsFlag(Rep)        = true;
                Clusts(Rep)           = NewClust;
                
                if(Rep == Rep1Idx)
                    %%% REMOVE NON-CLUSTER ASSOCIATED WITH Rep2Idx %%%
                    ClustsFlag(Rep2Idx) = false;
                    RepDMat(:, Rep2Idx) = UpperBd;
                    RepDMat(Rep2Idx, :) = UpperBd;
                    
                elseif(Rep == Rep2Idx)
                    %%% REMOVE NON-CLUSTER ASSOCIATED WITH Rep1Idx %%%
                    ClustsFlag(Rep1Idx) = false;
                    RepDMat(:, Rep1Idx) = UpperBd;
                    RepDMat(Rep1Idx, :) = UpperBd;
                    
                else
                    %%% REMOVE NON-CLUSTERS ASSOCIATED WITH Rep1Idx AND Rep2Idx %%%
                    ClustsFlag(Rep1Idx)    = false;
                    ClustsFlag(Rep2Idx)    = false;
                    RepDMat(:, Rep1Idx)   = UpperBd;
                    RepDMat(:, Rep2Idx)   = UpperBd;
                    RepDMat(Rep1Idx, :)   = UpperBd;
                    RepDMat(Rep2Idx, :)   = UpperBd;
                    
                end %%% if(Rep == Rep1Idx...
                
            end %%% if(length(NewClust.Idx...
            
            %%% UPDATE ROW AND COLUMN Rep OF RepDMat    %%%
            %%% SO Clusts(Rep) IS AVAILABLE FOR MERGING %%%
            RepDMat(1:B-1, Rep)   = SymKLDMat(1:B-1, Rep);
            RepDMat(Rep, B+1:end) = SymKLDMat(Rep, B+1:end);
            
            %%% MAKE ROWS & COLUMNS OF NON-CLUSTERS UNAVAILABLE %%%
            NotClustFlag          = (1-ClustsFlag);
            RepDMat(:, Rep)       = NotClustFlag *UpperBd;
            RepDMat(Rep, :)       = NotClustFlag'*UpperBd;
            GoodIdx               = find(ClustsFlag);
            RepDMat(GoodIdx, Rep) = SymKLDMat(GoodIdx, Rep);
            RepDMat(Rep, GoodIdx) = SymKLDMat(Rep, GoodIdx);
            RepDMat(Rep, Rep)     = UpperBd;
            
        end %%% if( (Nc == 1...
        
    end %%% while ((sum(ClustFlag...
    
    %%% REDUCE DIMENSIONALITY FROM B TO Nc %%%
    %%% USING AVERAGE OF BANDS IN EACH CLUSTER %%%
    if(Nc < B)
        ClustVecs = zeros(N, Nc);
        ClustIdx  = find(ClustsFlag);
        for c = 1:Nc;
            ClustVecs(:, c) = mean(X(:, Clusts(ClustIdx(c)).Idx), 2);
        end
    else
        ClustVecs = X;
    end
    
end %%% if(Nc & (Nc == B)) %%%

%%% ONLY KEEP THE TRUE CLUSTERS %%%
Clusts = Clusts(ClustsFlag);

%%
%%% ERROR CHECKING: %%%%
%%% MAKE SURE EACH WAVELENGTH IS ASSIGNED TO EXACTLY ONE CLUSTER %%%
ClustMems = zeros(Nc, B);
for c = 1:Nc
    ClustMems(c, Clusts(c).Idx) = 1;
end
SumMems = sum(ClustMems);
BigNum  = max(SumMems);
LitNum  = min(SumMems);
if (LitNum == 0)
    fprintf('Some Wavelength is not assigned to any Cluster\n');
    keyboard
elseif( BigNum > 1)
    fprintf('Some Wavelength is assigned to more than one Cluster\n');
    keyboard
elseif( ~((LitNum == 1) & (BigNum == 1)))
    fprintf('Something is wrong with the Cluster Memberships\n');
end

end %%% function [Clusts... %%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
%%%%%%%%%%%%%%%%%%%%%%%%
%%% HELPER FUNCTIONS %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [KLDivergences, Hists, UpperBd] = computeKLDivergencesBetweenBands(X, Wvs,Parameters);

%%% NORMALIZE X %%%
X = X/max(X(:));

%%% INITIALIZE PARAMETERS %%%
B          = size(X, 2);
SmScFac    = Parameters.SmScFac;
NBins      = Parameters.NBins;
Verbose    = Parameters.Verbose;
SmWindSz2  = Parameters.SmWindSz2;
SmoothHist = Parameters.SmoothHist;
SmWindSz   = 2*SmWindSz2+1;
NWvs       = size(X, 2);

%%% CONSTRUCT NORMALIZED HISTOGRAMS %%%
Centers  = [1/NBins:1/NBins:1];
SmallOne = SmScFac*ones(NBins, B);
Hists    = hist(X, Centers) + SmallOne;

%%% SMOOTH HISTOGRAM USING LOCAL AVERAGE FILTER OS SIZE SmWindSz %%%
if(SmoothHist)
    HistsSm        = conv2(Hists, (1/SmWindSz)*ones(SmWindSz,1), 'same');
    NormDen        = size(X, 1);
    SumHists       = sum(HistsSm);
    StInt          = 1:SmWindSz2;
    EdInt          = (NWvs-SmWindSz2+1):NWvs;
    DStart         = max(0, NormDen-SumHists(StInt))./255;
    DEnd           = max(0, NormDen-SumHists(EdInt))./255;
    Hists(:,StInt) = HistsSm(:, StInt) + DStart;
    Hists(:,EdInt) = HistsSm(:, EdInt) + DEnd;
end

%%
%%% COMPUTING SYMMETRIC KL-DIVERGENCE
%%% WE CAN USE THE HISTOGRAMS, AND NOT PDF'S,  IN KL %%%
%%% BECAUSE      %%%
%%%    ALL HISTS HAVE SAME NUMBER OF POINTS SO SCALING TO PDFs USES SAME DENOMINATOR FOR ALL    %%%
%%%    THE DENOMINATOR IS CONSTANT FACTOR IN THE RATIOS IN ARGUMENT OF log FUNCTIONS SO CANCELS %%%

KLDivergences = zeros(B, B);
for r = 1:B-1
    histr = Hists(:, r);
    pdfr  = histr/NormDen;
    for q = r+1:B
        histq              = Hists(:, q);
        pdfq               = histq/NormDen;
        KLDivergences(r,q) = sum(pdfq.*log(histq./histr)) + sum(pdfr.*log(histr./histq));
    end
end

%%% FILL LOWER TRIANGLE AND DIAGONAL OF KLDivergences TO LARGER VALUE THAT ALL DIVERGENCES %%%
UpperBd = 2*max(KLDivergences(:));
for r = 1:B;
    for q = 1:r;
        KLDivergences(r,q) = UpperBd;
    end
end

%%
%%% IF Verbose THEN DISPLAY HISTOGRAMS  %%%
if(Verbose)
    LastFnum = floor(min(B, 12*12)/12);
    if(LastFnum <= B) %%% TEMPORARY HACK!!!! %%%
        PlotSkip = 1;
    else
        PlotSkip = 12;
    end
    BigOnes  = max(Hists);
    BigOne   = max(BigOnes(12:PlotSkip:end));
    for mmm = 1:LastFnum;
        figure(mmm);
        NextOne = PlotSkip*mmm;
        bar((1/NormDen)*Hists(:, NextOne));
        ylim([0, BigOne]);
        title(sprintf('Wavelength Index %d', PlotSkip*mmm));
        drawnow
    end
    TileFigs(1:LastFnum, 0);
end

end %%% function [KLDivergences... %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [Clusts, ClustFlag] = MergeLastTwo(Clusts, ClustFlag, SymKLDMat, Wvs, B)
%function [Clusts] = MergeLastTwo(Clusts, ClustFlag, SymKLDMat)

%%% GET LAST TWO CLUSTS %%%
LastTwoIdx = find(ClustFlag);
Idx1       = LastTwoIdx(1);
Idx2       = LastTwoIdx(2);
Clust1     = Clusts(Idx1);
Clust2     = Clusts(Idx2);

%%% UPDATE CLUSTER 1 INDICES AND WAVELENGTHS %%%
Clust1.Idx = union(Clust1.Idx, Clust2.Idx);
Clust1.Wvs = Wvs(Clust1.Idx);

%%% FIND Rep MINIMIZING INTRA-CLUSTER DISTANCE %%%
Rep1       = Clust1.Rep;
Rep2       = Clust2.Rep;
MemsNot1   = setdiff(1:B, Rep1);
MemsNot2   = setdiff(1:B, Rep2);
IntClustD1 = min(SymKLDMat(Rep1, MemsNot1));
IntClustD2 = min(SymKLDMat(Rep2, MemsNot2));

%%% UPDATE CLUSTER 1 Rep
if(IntClustD1 < IntClustD2)
    Clust1.Rep       = Rep1;
    Clust1.RepWv     = Wvs(Rep1);
    Clust1.IntClustD = IntClustD1;
    ClustFlag(Rep2)  = false;
else
    Clust1.Rep       = Rep2;
    Clust1.RepWv     = Wvs(Rep2);
    Clust1.IntClustD = IntClustD2;
end

%%% FINALIZE Clusts AND ClustFlag %%%
Clusts(1)      = Clust1;
ClustFlag(1)   = true;
ClustFlag(2:B) = false;

end
%%% OF FUNCTION MergeLastTwo %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
