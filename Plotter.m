% Enter your MATLAB code below
readChId =              % Your Channel ID					
readKey = '' %Your Read API Key
[Data1, Time1] = thingSpeakRead(readChId,'fields',[1,4,3,2,5],...
    'NumPoints',500,'ReadKey',readKey);

[Data2, Time2] = thingSpeakRead(readChId,'fields',[6],...
    'NumPoints',500,'ReadKey',readKey);


%% title('Temperature and Humidity'); %%


%% Temperature and Humidity Plots %%
%%yyaxis left;%%
plot(Time1, Data1);
ylabel('Temprature and Humidity');
xlabel('Date & Time (GMT+0)');

%% Pressure Plots %%
yyaxis right;
plot(Time2, Data2);
ylabel('Pressure');

legend({'Temp DDT11 (C)','Temp BME280 (C)','Temp ESP32 (C)','Hum DDT11 (%)','Hum BME280 (%)','Pres BME280 (hPa)'});
legend('Location','best')

grid on;
