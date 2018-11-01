function [Parameters] = HierarchClusterByDGParameters();

Parameters.Nc         = 4;                          %Number of Clusters
Parameters.NBins      = 255;                        %Number of bins in reflectance histograms
Parameters.MaxIters   = 2581;                       %Arbitrary number of maximum interations
Parameters.SmScFac    = eps*10^8;                   %Amount to add to bins to avoid divide by 0
LogSm                 = log(Parameters.SmScFac);    %Tmp variable used in next line
Parameters.UpperBd    = -LogSm-10;                  %Amount to add to lower triangle of distmatrix
Parameters.Verbose    = false;                      %if true, display histograms
Parameters.SmoothHist = true;                       %if true, smooth histograms with local average
Parameters.SmWindSz2  = 2;                          %size of local ave window is 2*SmWindSz2+1