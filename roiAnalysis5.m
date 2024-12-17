%clear;
warning('off','MATLAB:polyshape:repairedBySimplify')
zipFileToExtract = "redone measurements.zip";
disp(zipFileToExtract)
[fileNames_py,coordList_py] = pyrunfile("test.py '" + zipFileToExtract + "'",["fileNames","coordList"]);
% fileNames is the list of ROI file names, not the list of zip file names
% that contain ROIs

rotMatrix = @(theta)[cos(deg2rad(theta)),-sin(deg2rad(theta));sin(deg2rad(theta)),cos(deg2rad(theta))];
yintercept = @(x1,y1,x2,y2) -x1*((y2-y1)/(x2-x1))+y1;

fileNames = string(fileNames_py);
allROIs = cell(coordList_py);
for inc = [1:length(allROIs)]
    % removing exclusion regions
%     if fileNames(inc) == "1926-0531.roi"
%         continue
%     end
%     if fileNames(inc) == "2676-1896.roi"
%         continue
%     end
%     if fileNames(inc) ~= "2.roi"
%         continue
%     end

    %disp(inc)
    % Extracting the data produced by the python program
    roiPyList = allROIs(inc);
    numOfPoints = max(size(roiPyList{1}).*[0,1]);
    %1-liner to get the number of columns ^
    roiMlMatrix = zeros(numOfPoints,2);
    for j = [1:numOfPoints]
        roiMlMatrix(j,:) = double(roiPyList{1}{j});
    end
    % Creating a polyshape for the current ROI
    % This allows us to find the center of the particle, which is important
    % for rotating it to measure diameter from every angle
    particle = polyshape(roiMlMatrix(:,1),roiMlMatrix(:,2));
    [x_c,y_c] = centroid(particle);
    % x and y are the variables that really matter. These outline the
    % particle, with the particle center at 0,0;
    x = roiMlMatrix(:,1)-x_c;
    y = roiMlMatrix(:,2)-y_c;
    
    % now that we have the outline of the particle, we can measure its
    % diameter
    % pv: particle vector. This refers to a list of vectors, each pointing
    % from the origin to a point on the outline of the particle
    pv = [x';y'];
    %diameter = [];
    %hold on
    
    %% once the data is imported

    % change the second value to take more/fewer measurements per particle
    for deg = [0:30:299];
        pvr = [0;0];
        % This itterates over pv, multiplying each vector in it by a
        % rotation matrix.
        for knc = [1:length(pv)]
            pvr(:,knc) = rotMatrix(deg)*pv(:,knc);
        end
        pvr = [pvr,pvr(:,1)];
        
        % This checks where in the list of points the x-values change sign.
        % If the x-value goes from positive to negative (or negative to
        % positive) from one point to the next, the line connecting those
        % points must cross the y-axis. The y-intercept of this line is
        % calculated and recorded in pointList
        prevSign = sign(pvr(1,1));
        pointList = [];
        for jnc = [1:length(pvr)]
            if pvr(1,jnc) == 0
                disp("")
                fprintf("Point on the y-axis: %s, Pt %d @ %d°\n",fileNames(inc),jnc,deg)
                continue
            end
            if prevSign ~= sign(pvr(1,jnc))
                pointList = [pointList,yintercept(pvr(1,jnc-1),pvr(2,jnc-1),pvr(1,jnc),pvr(2,jnc))];
                prevSign = sign(pvr(1,jnc));
                %Set a break point in the code
            end
        end
        
        %if deg == 0
            % I use this section of code to visualize an ROI, along with a
            % breakpoint on the end statement for the value of inc
            % corresponding to the ROI I want to examine.
            % I have it set as deg == 400 when I don't want to visualize
            % any ROIS
%             hold on
%             plot(polyshape(pvr(1,:),pvr(2,:)))
%             scatter(zeros(1,length(pointList)),pointList,150,"rx",'LineWidth',1.5)
%             %scatter(pvr(1,1),pvr(2,1),"kx")
%             scatter(0,0,50,"ko",'LineWidth',1.5)
%             plot(zeros(length(-250:250),1),-250:250,"k--",'LineWidth',1.5)
%             xlim([-250,250])
%             ylim([-250,250])
%             xlabel("position (nm)")
%             ylabel("position (nm)")
%             axis square
        %end
        
        % The highest and lowest values in pointList are subtracted, giving
        % the full diameter of the particle
        % diameter = [diameter,max(pointList)-min(pointList)];
        disp(deg)
        disp(max(pointList)-min(pointList))
        %fi = fopen("C:\Users\jonme\Documents\School Work\Research - Bowman Lab\image analysis\roi python testing\600CDiameters.txt","a");
        % fi for file identifier
        %fprintf(fi,'%s,%s,%u,%f\n',zipFileToExtract,fileNames(inc),deg,max(pointList)-min(pointList));
        %fclose(fi);
    end
    % This is actually a 2D matrix with rows of varying length
    %diameterList = [diameter;diameterList];
    % This is a 1D list
    %diameterMeanList = [mean(diameter);diameterMeanList];
    %fprintf("%s,%s,%f,%f,%u\n",zipFileToExtract,fileNames(inc),mean(diameter),std(diameter),length(diameter))
end