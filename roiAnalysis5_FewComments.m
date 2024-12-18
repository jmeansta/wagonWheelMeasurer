%clear;
warning('off','MATLAB:polyshape:repairedBySimplify')
zipFileToExtract = "redone measurements.zip";
disp(zipFileToExtract)
[fileNames_py,coordList_py] = pyrunfile("test.py '" + zipFileToExtract + "'",["fileNames","coordList"]);

rotMatrix = @(theta)[cos(deg2rad(theta)),-sin(deg2rad(theta));sin(deg2rad(theta)),cos(deg2rad(theta))];
yintercept = @(x1,y1,x2,y2) -x1*((y2-y1)/(x2-x1))+y1;

fileNames = string(fileNames_py);
allROIs = cell(coordList_py);
for inc = [1:length(allROIs)]
    % Reading data in
    roiPyList = allROIs(inc);
    numOfPoints = max(size(roiPyList{1}).*[0,1]);
    roiMlMatrix = zeros(numOfPoints,2);
    for j = [1:numOfPoints]
        roiMlMatrix(j,:) = double(roiPyList{1}{j});
    end

    % Creating a particle with its centroid at the origin
    particle = polyshape(roiMlMatrix(:,1),roiMlMatrix(:,2));
    [x_c,y_c] = centroid(particle);
    x = roiMlMatrix(:,1)-x_c;
    y = roiMlMatrix(:,2)-y_c;

    % formatting
    pv = [x';y'];
    % pv = particle vector.
    % At this stage, each point on the particle's polyline is considered a vector from the origin
    % In the next stage, each vector will be multiplied by a rotation matrix

    for deg = [0:30:299];
        % rotation
        pvr = [0;0];
        for knc = [1:length(pv)]
            pvr(:,knc) = rotMatrix(deg)*pv(:,knc);
        end

        pvr = [pvr,pvr(:,1)]; % appending a copy of the first point to make a closed polygon
        prevSign = sign(pvr(1,1)); % Initializing prevSign
        pointList = [];

        % Itterating over each vector
        % This finds the point on the particle's outline that is on the y axis
        % Because the outline has been rotated, this makes up the "wagon wheel" effect
        for jnc = [1:length(pvr)]
            if pvr(1,jnc) == 0
                disp("")
                fprintf("Point on the y-axis: %s, Pt %d @ %d°\n",fileNames(inc),jnc,deg)
                continue
            end
            if prevSign ~= sign(pvr(1,jnc))
                pointList = [pointList,yintercept(pvr(1,jnc-1),pvr(2,jnc-1),pvr(1,jnc),pvr(2,jnc))];
                prevSign = sign(pvr(1,jnc));
            end
        end

        % There may be more than 2 points on the particle's outline that lie on the y-axis
        % Ex: Think of a particle shaped like the letter C.
        % A vertical line would go in and out of the C-shaped particle twice
        % Thus, the maximum and minimum from the list of points are used to find the greatest diameter
        disp(deg)
        disp(max(pointList)-min(pointList))
    end
end