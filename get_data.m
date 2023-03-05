for i = 1:16 
data_path = "sub"+i+"_data.csv";
event_path = "sub"+i+"_event.csv";
label_data = "sub"+i+"_event.csv";
csvwrite(data_path, data{1,i}.trial{1,1});
%writetable(struct2table(event{1,i}), "sub"+i+"_event.csv");
%writetable(cell2table(data{1,i}.label), "sub"+i+"_label.csv");
end