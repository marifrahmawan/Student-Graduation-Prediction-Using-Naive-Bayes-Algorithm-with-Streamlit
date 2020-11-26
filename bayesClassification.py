import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from openpyxl import load_workbook


def proccesClassification(allData,split_tt):
	for index, row in allData.iterrows():	
		if row ['PRODI'] == "TEKNIK ELEKTRO":
			rs = 15
			piechartName = "TEKNIK ELEKTRO"
		elif row ['PRODI'] == "TEKNIK INDUSTRI":
			rs = 37
			piechartName = "TEKNIK INDUSTRI"
		elif row ['PRODI'] == "TEKNIK INFORMATIKA":
			rs = 32
			piechartName = "TEKNIK INFORMATIKA"
		elif row ['PRODI'] == "TEKNIK KIMIA":
			rs = 13
			piechartName = "TEKNIK KIMIA"
	
		

	model = GaussianNB()
	st.write("***Data Training dan Testing***")
	x = allData[['ASAL SEKOLAH', 'PROVINSI', 'KUANT. MATE']]
	st.write(x)

	st.write("***Data Target***")
	y = allData['STATUS KELULUSAN']
	st.write(y)
	st.write(y.shape)

	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = split_tt, random_state=rs) # 52019, 1230, 7, 12/13/14/15, industri = 37, elektro = 15, informatika = 32, kimia = 13, test = 230
	nbtrain = model.fit(x_train, y_train)

	st.markdown('***DATA TRAINING : ***')
	st.write(x_train)
	st.write(x_train.shape)

	st.markdown('***TARGET TRAINING : ***')
	st.write(y_train)
	st.write(y_train.shape)

	st.markdown('***DATA TESTING : ***')
	st.write(x_test)
	st.write(x_test.shape)

	st.markdown('***TARGET TESTING : ***')
	st.write(y_test)
	st.write(y_test.shape)

	y_pred = nbtrain.predict(x_test)
	st.write("***Hasil Prediksi***")
	st.write(y_pred)
	st.write(y_pred.shape)

	st.write("***Data Porbabilitas Prediksi***")
	predic_prob = nbtrain.predict_proba(x_test)
	st.write(predic_prob)

    # Confusion matrix
	st.write("***Confusion Matrix***")
	df_confusion = pd.crosstab(y_test, y_pred)
	st.write(df_confusion)

	report = classification_report(y_test, y_pred)
	st.text(report)

	hasilTest = pd.DataFrame(y_pred)
	testTepat = hasilTest.apply(lambda x: True if x[0] == "TEPAT" else False , axis=1)
	testTidakTepat = hasilTest.apply(lambda x: True if x[0] == "TIDAK TEPAT" else False , axis=1)
	jumlahTestTepat = len(testTepat[testTepat == True].index)
	jumlahTestTidakTepat = len(testTidakTepat[testTidakTepat == True].index)

	Data = {piechartName: [jumlahTestTepat,jumlahTestTidakTepat]}
	df = pd.DataFrame(Data,columns=[piechartName],index = ['Tepat','Tidak Tepat'])
	df.plot.pie(y=piechartName,figsize=(10,6), autopct='%1.0f%%', startangle=60)
	TestChart = plt.show()
	st.pyplot(TestChart)

	uploadDataUji = st.file_uploader("Choose a Excel file", type=['csv','xlsx'], key = 'b')
	if uploadDataUji is not None:
		st.write("***Data Mahasiswa***")
		wb = load_workbook(uploadDataUji)
		sheet_ranges = wb["Sheet1"]
		model = GaussianNB()
		datamhs = pd.DataFrame(sheet_ranges.values)
		datamhs = datamhs[datamhs != 0]

		jml_row = datamhs[0].count()

		cleaning_mhs = datamhs[1:jml_row][[1,2,3,4,5,6]]
		cleaning_mhs.columns = ['NIM', 'NAMA', 'ASAL SEKOLAH', 'PRODI', 'PROVINSI', 'RATA MATE']
		# menghapus data noise
		cleaning_mhs = cleaning_mhs.dropna(axis=0, how='any')

		# mengubah tipe data dari object ke float
		cleaning_mhs['RATA MATE'] = cleaning_mhs['RATA MATE'].apply(str)
		cleaning_mhs['RATA MATE'] = cleaning_mhs['RATA MATE'].str.replace(',','.').apply(float)

		for index, row in cleaning_mhs.iterrows():
			# RATA MATE MATIKA
			if row['RATA MATE'] >= 93 and row['RATA MATE'] <= 100:
				cleaning_mhs.loc[index,'KUANT. MATE'] = 'SANGAT BAIK'
			elif row['RATA MATE'] >= 84 and row['RATA MATE'] <= 92:
				cleaning_mhs.loc[index,'KUANT. MATE'] = 'BAIK'
			elif row['RATA MATE'] >= 75 and row['RATA MATE'] <= 83:
				cleaning_mhs.loc[index,'KUANT. MATE'] = 'CUKUP'
			elif row['RATA MATE'] >= 0 and row['RATA MATE'] <= 74:
				cleaning_mhs.loc[index,'KUANT. MATE'] = 'PERLU DIMAKSIMALKAN'
			
		cleaning_mhs
		transformasi_mhs = cleaning_mhs[['NIM', 'NAMA','ASAL SEKOLAH', 'PROVINSI', 'KUANT. MATE']]
		for index, row in transformasi_mhs.iterrows():
			if 'Maluku Utara' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '1'
			elif 'Kalimantan Tengah' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '1'

			elif 'Banten' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Yogyakarta' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Gorontalo' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Bengkulu'in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Kalimantan Selatan' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Lampung' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Sumatera' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Riau' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Sulawesi' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Nusa Tenggara' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Aceh' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Bangka' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Kalimantan Barat' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Jawa' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'jawa' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Jambi' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Jakarta' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Bali' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			elif 'Kalimantan Utara' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '2'
			
			elif 'Papua' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '3'
			elif 'Kalimantan Timur' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '3'
			elif 'Maluku' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '3'
			elif 'lain' in row['PROVINSI']:
				transformasi_mhs.loc[index, 'PROVINSI'] = '3'
			
			#ASAL SEOKLAH
			if 'SMA' in row['ASAL SEKOLAH'] or 'sma' in row['ASAL SEKOLAH'] or 'Sma' in row['ASAL SEKOLAH'] or 'SMTA' in row['ASAL SEKOLAH']:
				transformasi_mhs.loc[index, 'ASAL SEKOLAH'] = '1'
			elif 'SMK' in row['ASAL SEKOLAH'] or 'smk' in row['ASAL SEKOLAH'] or 'Smk' in row['ASAL SEKOLAH'] or 'STM' in row['ASAL SEKOLAH'] or 'SMF' in row['ASAL SEKOLAH']:
				transformasi_mhs.loc[index, 'ASAL SEKOLAH'] = '2'
			elif 'MA' in row['ASAL SEKOLAH'] or 'Ma' in row['ASAL SEKOLAH']:
				transformasi_mhs.loc[index, 'ASAL SEKOLAH'] = '3'
			
			# RATA MATEMATIKA
			if row['KUANT. MATE'] == "SANGAT BAIK":
				transformasi_mhs.loc[index,'KUANT. MATE'] = 4
			elif row['KUANT. MATE'] == "BAIK":
				transformasi_mhs.loc[index,'KUANT. MATE'] = 3
			elif row['KUANT. MATE'] == "CUKUP":
				transformasi_mhs.loc[index,'KUANT. MATE'] = 2
			elif row['KUANT. MATE'] == "PERLU DIMAKSIMALKAN":
				transformasi_mhs.loc[index,'KUANT. MATE'] = 1
			
			dataPrediksi = transformasi_mhs[['ASAL SEKOLAH', 'PROVINSI', 'KUANT. MATE']]

		ass = cleaning_mhs[['NIM', 'NAMA','ASAL SEKOLAH', 'PROVINSI', 'KUANT. MATE']]
		model.fit(x_train, y_train)
		nbtrain = model.fit(x_train, y_train)
		st.write(pd.DataFrame(transformasi_mhs))
		dataPrediksi = pd.DataFrame(dataPrediksi)
		
		# lbr = len(ddd.columns)
		# st.write(lbr)

		pjg = len(dataPrediksi)
		dindex = []
		for i in range(pjg):
			dindex.append(int(i+1))
		# ddd.set_axis(dindex,axis='index')
		# st.write(ddd)
		prediksi = model.predict(dataPrediksi)
		
		prediksi = pd.DataFrame(prediksi)
		prediksi.set_axis(dindex,axis='index')

		prediksi_prob = nbtrain.predict_proba(dataPrediksi)
		prediksi_prob = pd.DataFrame(prediksi_prob)
		prediksi_prob.set_axis(dindex,axis='index')

		df_index = pd.merge(ass, prediksi_prob, right_index=True, left_index=True)
		lastTable = pd.merge(df_index, prediksi, right_index=True, left_index=True)
		st.write("***Hasil Prediksi***")
		st.write(lastTable)

		Obj1 = lastTable.apply(lambda x: True if x['0_y'] == "TEPAT" else False , axis=1)
		Obj2 = lastTable.apply(lambda x: True if x['0_y'] == "TIDAK TEPAT" else False , axis=1)
		jumlahTepat = len(Obj1[Obj1 == True].index)
		jumlahTidakTepat = len(Obj2[Obj2 == True].index)

		st.write("***Mahasiswa Lulus Tepat Waktu " + str(jumlahTepat) + " ***")
		st.write("***Mahasiswa Lulus Tidak Tepat Waktu " + str(jumlahTidakTepat) + " ***")
		Data = {piechartName: [jumlahTepat,jumlahTidakTepat]}
		df = pd.DataFrame(Data,columns=[piechartName],index = ['Tepat','Tidak Tepat'])
		df.plot.pie(y=piechartName,figsize=(10, 6),autopct='%1.0f%%', startangle=60)
		bayesChart = plt.show()
		st.pyplot(bayesChart)

	else:
		st.write('UPLOAD FILE YANG AKAN DIPREDIKSI')

	
	
	# for index, row in dataPrediksi.iterrows():
	# 	prediksi = model.predict([row])
	# 	prediksi_prob = nbtrain.predict_proba([row])
	# 	st.write(row.count())