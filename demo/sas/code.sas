/* SAS example for data analysis */
data sample_data;
    do i = 1 to 1000;
        feature1 = rand('NORMAL', 0, 1);
        feature2 = rand('NORMAL', 1, 2);
        feature3 = rand('EXPONENTIAL', 2);
        target = rand('BERNOULLI', 0.3);
        output;
    end;
    drop i;
run;

/* Data exploration */
proc means data=sample_data;
    var feature1 feature2 feature3;
run;

proc freq data=sample_data;
    tables target;
run;

/* Visualization */
proc sgplot data=sample_data;
    histogram feature1 / transparency=0.7;
    density feature1;
    title "Feature 1 Distribution";
run;

proc sgplot data=sample_data;
    histogram feature2 / transparency=0.7;
    density feature2;
    title "Feature 2 Distribution";
run;

proc sgplot data=sample_data;
    histogram feature3 / transparency=0.7;
    density feature3;
    title "Feature 3 Distribution";
run;

/* Machine Learning */
proc hpsplit data=sample_data;
    class target;
    model target = feature1 feature2 feature3;
    partition fraction(validate=0.2 seed=42);
    output out=predicted;
run;

/* Model evaluation */
proc freq data=predicted;
    tables target*_into_ / nopercent nocol;
run;
