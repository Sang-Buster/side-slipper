% this script plots individual segments
% and is called by:
%   plot_segments.m
%
% which is called by:
%   postproc.m
%
% Marc Compere, comperem@erau.edu
% created : 09 Jul 2024
% modified: 08 Sep 2024

grn =[0.3,0.8,0.5]; % nicer green
grn2=[0.4 0.8 0.07];

idx_for_seg  = idx_this_segment{seg}; % indices into N_ vectors for this segment 

N_extents = [min(N_extents(1),min(N_cg(idx_for_seg))) max(N_extents(2),max(N_cg(idx_for_seg)))];
E_extents = [min(E_extents(1),min(E_cg(idx_for_seg))) max(E_extents(2),max(E_cg(idx_for_seg)))];
plot(N_cg   (idx_for_seg), E_cg  (idx_for_seg) , 'Color',cmap(k,:),'Marker','.')
plot(N_rear(idx_for_seg), E_rear(idx_for_seg) , 'Color',cmap(k+1,:),'Marker','.')
legend_str{k} = sprintf('Segment #%i, length: %6.1f(m)',k,S_tot{seg});

% rover velocity vector at CG
gps_cg_COG     = (pi/180)*rover_CoG( idx_for_seg ); % (rad) from (deg)
gps_cg_spd_mps = rover_spd(idx_for_seg); % (m/s)
vel_cg_XY      = gps_cg_spd_mps.*[cos(gps_cg_COG), sin(gps_cg_COG)]; % (m/s) from body-fixed to terrain-fixed frame; 1mph=0.44704(m/s)

% chassis orientation scaled by rover velocity vector at CG
chassis_psi    = (pi/180)*rover_heading( idx_for_seg ); % (rad) from (deg) vehicle heading as measured by RTK GPS rover at CG w.r.t. moving base at rear axle
chassis_psi_XY = gps_cg_spd_mps.*[cos(chassis_psi), sin(chassis_psi)]; % (m/s) from body-fixed to terrain-fixed frame; 1mph=0.44704(m/s)

% base velocity vector at rear axle
gps_rear_COG     = (pi/180)*base_CoG( idx_for_seg ); % (rad) from (deg)
gps_rear_spd_mps = base_spd(idx_for_seg); % (m/s)
vel_rear_XY      = gps_rear_spd_mps.*[cos(gps_rear_COG), sin(gps_rear_COG)]; % (m/s) from body-fixed to terrain-fixed frame; 1mph=0.44704(m/s)



%% create time history plots for this segment's GPS and IMU and INS data
% %ret = plot_time_history_for_this_segment(k,seg,idx_for_seg,idx2_for_seg);
% if plot_time_histories>0
%     %h_outerLoop=gcf; % store this to restore it after this time history interlude 
%     plot_time_history_for_this_segment
%     figure(h_outerLoop) % restore outer-loop current figure
% end % if plot_time_histories>0


% plot velocity vectors at each point
sf=1; %*0.3; % scaleFactor for vel, to improve visuals only
pt1_cg=[N_cg(idx_for_seg)                   , E_cg(idx_for_seg)                     ]; % (m) tail, or base of arrow
pt2_cg=[N_cg(idx_for_seg)+sf*vel_cg_XY(:,1) , E_cg(idx_for_seg)+sf*vel_cg_XY(:,2)]; % (m) with vel (m/s) as magnitude, tip, or end of arrow

pt1_chassis=[N_cg(idx_for_seg)                        , E_cg(idx_for_seg)                       ]; % (m) tail, or base of arrow
pt2_chassis=[N_cg(idx_for_seg)+sf*chassis_psi_XY(:,1) , E_cg(idx_for_seg)+sf*chassis_psi_XY(:,2)]; % (m) chassis orientation vector with vel (m/s) as magnitude, tip, or end of arrow

pt1_rear=[N_rear(idx_for_seg)                       , E_rear(idx_for_seg)                     ]; % (m) tail, or base of arrow
pt2_rear=[N_rear(idx_for_seg)+sf*vel_rear_XY(:,1)   , E_rear(idx_for_seg)+sf*vel_rear_XY(:,2) ]; % (m) with vel (m/s) as magnitude, tip, or end of arrow

skipNth=4;
%skipNth=1;
m = min( length(pt1_cg) , length(pt1_rear) ); % sometimes front and rear GPS length arrays are different lengths by 1 element
for i=1:skipNth:m
    drawArrow(pt1_cg(i,:)     , pt2_cg(i,:)     ,'linewidth',0.5,'color','b')
    drawArrow(pt1_chassis(i,:), pt2_chassis(i,:),'linewidth',0.5,'color',grn); % grn or grn2
    drawArrow(pt1_rear(i,:)   , pt2_rear(i,:)   ,'linewidth',0.5,'color','r')
    plot(pt1_cg(i,1),pt1_cg(i,2),'bo','MarkerSize',6)
    plot(pt1_rear(i,1),pt1_rear(i,2),'ro','MarkerSize',6)
    %text(pt1_front(i,1),pt1_front(i,2),num2str(i),'VerticalAlignment','bottom','HorizontalAlignment','center');
    %text(pt1_rear(i,1),pt1_rear(i,2),num2str(i),'VerticalAlignment','bottom','HorizontalAlignment','center');
end % for i=1:skipNth:length(pt1_rear)


legend_str{seg} = sprintf('Segment #%i',seg);
text( mean(N_cg(idx_for_seg)),mean(E_cg(idx_for_seg)),legend_str{seg},...
    'HorizontalAlignment','center','VerticalAlignment','bottom','Color',cmap(k,:));




xlabel('SAE X, UTM Northing (m)')
ylabel('SAE Y, UTM Easting (m)')
grid on
axis equal
title( strcat( sprintf('k=%d, seg=%d,  ',k,seg), description_str ) )
%myAxes=axis
myAxLim = [N_extents, E_extents];
axis([myAxLim(1) myAxLim(2) myAxLim(3) myAxLim(4)]);
zoom(0.6) % zoom out a bit
%axFac=1.01; %1.01; %0.99;
%axis([(1/axFac)*myAxLim(1) axFac*myAxLim(2) (1/axFac)*myAxLim(3) axFac*myAxLim(4)]);
%axis([ -3944.3      -3401.7      -3174.8      -2745.5    -0.061337     0.061337])
    

            








