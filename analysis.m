clear, close all

load('series.mat')

series = series(:, 1:8);
base = series(2, :);
series = series(3: length(series), :);
series_len = length(series);

on = series(:, 1);
off_a = series(:, 2);
off_b = series(:, 4);
off_c = series(:, 6);
off_d = series(:, 8);

label = [on, off_a, off_b, off_c, off_d];
label_name = ['on   '; 'off_a'; 'off_b'; 'off_c'; 'off_d'];
label_name_string = cellstr(label_name);
combs = combntns([1, 2, 3, 4, 5],2);

for i = 1: length(combs)    
    figure, plot(label(:, combs(i, 1)), label(:, combs(i, 2)), '.');
    xlabel(label_name_string(combs(i, 1)));
    ylabel(label_name_string(combs(i, 2)));
end

cov(label, 1)
corrcoef(label)

for i = 1:series_len
    series(i, :) = series(i, :) ./ base;
end

series = series - 1;

% index = [1: series_len]';

% middle = ones(1, series_len);
% low = -0.1 * middle;
% high = 0.1 * middle;
% 
% figure, bar(series(:, 1));
% hold on
% plot(low, 'r');
% % plot(middle, 'y');
% plot(high, 'r');
% xlim([1 series_len])
% ylim([-0.2 0.2])
% title('HBV on-rate')
% 
% for i = 1: 4
%     figure, bar(series(:, i * 2));
%     hold on
%     plot(low, 'r');
% %     plot(middle, 'y');
%     plot(high, 'r');
%     xlim([1 series_len])
%     ylim([-0.4 0.3])
%     title('HBV off-rate') 
%     ylabel(label_name_string(i + 1));
% end