for num_user in 40 60 80 100;
do
	python src/generator.py data/carpool_graphs/threshold_R51_0.3.graphml out/exp_skew $num_user 0 50 50 1 data/excel_template/template.xlsm
	python src/generator.py data/carpool_graphs/threshold_R51_0.3.graphml out/exp_skew $num_user 1 50 50 1 data/excel_template/template.xlsm
	python src/generator.py data/carpool_graphs/threshold_R51_0.3.graphml out/exp_skew $num_user 2 50 50 1 data/excel_template/template.xlsm
	python src/generator.py data/carpool_graphs/threshold_R51_0.3.graphml out/exp_skew $num_user 3 50 50 1 data/excel_template/template.xlsm
	python src/generator.py data/carpool_graphs/threshold_C51_0.5.graphml out/exp_skew $num_user 0 50 50 1 data/excel_template/template.xlsm
done