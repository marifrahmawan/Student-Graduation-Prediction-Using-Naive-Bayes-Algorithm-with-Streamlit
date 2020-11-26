import streamlit as st
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

st.title('Prediksi Kelulusan Mahasiswa Dengan Naive Bayes')
nim = st.text_input('Masukkan NIM Mahasiswa')
split_tt = st.sidebar.slider("Split Data Training dan Testing", min_value = 0.1, max_value = 0.99)

prov = st.sidebar.selectbox(
    'Asal Provinsi',
    ('Maluku Utara', 'Kalimantan Tengah', 'Banten', 'Yogyakarta', 'Gorontalo', 'Bengkulu', 'Kalimantan Selatan', 'Lampung', 'Sumatera', 'Riau', 'Sulawesi', 'Nusa Tenggara', 'Aceh', 'Bangka', 'Kalimantan Barat', 'Jawa', 'Jambi', 
	'Jakarta', 'Bali', 'Kalimantan Utara', 'Papua', 'Kalimantan Timur', 'Maluku', 'Lain - lain')
)
asalSekolah = st.sidebar.selectbox(
    'Asal Sekolah',
    ('SMA', 'SMK', 'MA')
)

# umur = st.sidebar.slider("Umur saat masuk", min_value = 17, max_value = 22)
rata_matematika = st.sidebar.slider("Rata-rata Matematika", min_value = 0, max_value = 100)
ipk = st.sidebar.slider("IPK", min_value = 0.00, max_value = 4.00)
toefl = st.sidebar.slider("TOEFL", min_value = 400, max_value = 600)

if prov == 'Maluku Utara':
	prov = 1
elif prov == 'Kalimantan Tengah':
	prov = 1

elif prov == 'Banten':
	prov = 2
elif prov == 'Yogyakarta':
	prov = 2
elif prov == 'Gorontalo':
	prov = 2
elif prov == 'Bengkulu':
	prov = 2
elif prov == 'Kalimantan Selatan':
	prov = 2
elif prov == 'Lampung':
	prov = 2
elif prov == 'Sumatera':
	prov = 2
elif prov == 'Riau':
	prov = 2
elif prov == 'Sulawesi':
	prov = 2
elif prov == 'Nusa Tenggara':
	prov = 2
elif prov == 'Aceh':
	prov = 2
elif prov == 'Bangka':
	prov = 2
elif prov == 'Kalimantan Barat':
	prov = 2
elif prov == 'Jawa':
	prov = 2
elif prov == 'Jambi':
	prov = 2
elif prov == 'Jakarta':
	prov = 2
elif prov == 'Bali':
	prov = 2
elif prov == 'Kalimantan Utara':
	prov = 2

elif prov == 'Papua':
	prov = 3
elif prov == 'Kalimantan Timur':
	prov = 3
elif prov == 'Maluku':
	prov = 3
elif prov == 'Lain - lain':
	prov = 3

if asalSekolah == 'SMA':
	asalSekolah = 1
elif asalSekolah == 'SMK':
	asalSekolah = 2
elif asalSekolah == 'MA':
	asalSekolah = 3

if rata_matematika >= 93 and rata_matematika <= 100:
	rata_matematika = 4
elif rata_matematika >= 84 and rata_matematika <= 92:
	rata_matematika = 3
elif rata_matematika >= 75 and rata_matematika <= 83:
	rata_matematika = 2
elif rata_matematika >= 0 and rata_matematika <= 74:
	rata_matematika = 1

if ipk >= 3.51 and ipk <= 4.00:
	ipk = 4
elif ipk >= 3.01 and ipk <= 3.50:
	ipk = 3
elif ipk >= 2.76 and ipk <= 3.00:
	ipk = 2
elif ipk >= 0.00 and ipk <= 2.75:
	ipk = 0

if toefl <= 400.0:
	toefl = 1
elif toefl >= 401.0 and toefl <= 420.0:
	toefl = 2
elif toefl >= 421.0 and toefl <= 440.0:
	toefl = 3
elif toefl >= 441.0 and toefl <= 460.0:
	toefl = 4
elif toefl >= 461.0 and toefl <= 480.0:
	toefl = 5
elif toefl >= 481.0 and toefl <= 500.0:
	toefl = 6
elif toefl >= 501.0 and toefl <= 520.0:
	toefl = 7
elif toefl >= 521.0 and toefl <= 540.0:
	toefl = 8
elif toefl >= 541.0 and toefl <= 560.0:
	toefl = 9
elif toefl >= 561.0 and toefl <= 580.0:
	toefl = 10
elif toefl >= 581.0 and toefl <= 600.0:
	toefl = 11

uploaded_file = st.file_uploader("Choose a Excel file", type=['csv','xlsx'])
if uploaded_file is not None:
	st.write("***Data Mahasiswa***")
	wb = load_workbook(uploaded_file)
	sheet_ranges = wb["Sheet1"]

	datamhs = pd.DataFrame(sheet_ranges.values)
	datamhs = datamhs[datamhs != 0]

	datamhs

	st.write("***Jumlah Data Awal***")
	datamhs.shape
	jml_row = datamhs[0].count()

	cleaning_mhs = datamhs[1:jml_row][[1,2,3,4,5,6,9,10,11]]
	st.write("***Data Cleaning***")
	cleaning_mhs.columns = ['NIM', 'NAMA', 'ASAL SEKOLAH', 'PRODI', 'PROVINSI', 'RATA MATE', 'IPK', 'TOEFL','LAMA STUDI']
	# menghapus data noise
	
	cleaning_mhs = cleaning_mhs.dropna(axis=0, how='any')
	cleaning_mhs

	st.write("***Jumlah Data Setelah Cleaning***")
	cleaning_mhs.shape

	# mengubah tipe data dari object ke float
	cleaning_mhs['RATA MATE'] = cleaning_mhs['RATA MATE'].apply(str)
	cleaning_mhs['RATA MATE'] = cleaning_mhs['RATA MATE'].str.replace(',','.').apply(float)
	cleaning_mhs['IPK'] = cleaning_mhs['IPK'].apply(str)
	cleaning_mhs['IPK'] = cleaning_mhs['IPK'].str.replace(',','.').apply(float)
	cleaning_mhs['TOEFL'] = cleaning_mhs['TOEFL'].apply(str)
	cleaning_mhs['TOEFL'] = cleaning_mhs['TOEFL'].str.replace(',','.').apply(float)


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
		
		# IPK
		if row['IPK'] >= 3.51 and row['IPK'] <= 4:
			cleaning_mhs.loc[index, 'KUANT. IPK'] = 'ISTIMEWA'
		elif row['IPK'] >= 3.01 and row['IPK'] <= 3.50:
			cleaning_mhs.loc[index, 'KUANT. IPK'] = 'BAIK'
		elif row['IPK'] >= 2.76 and row['IPK'] <= 3.00:
			cleaning_mhs.loc[index, 'KUANT. IPK'] = 'CUKUP'
		elif row['IPK'] >= 0.00 and row['IPK'] <= 2.75:
			cleaning_mhs.loc[index, 'KUANT. IPK'] = 'KURANG'

		#TOEFL
		if row['TOEFL'] <= 400.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 1'
		elif row['TOEFL'] >= 401.0 and row['TOEFL'] <= 420.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 2'
		elif row['TOEFL'] >= 421.0 and row['TOEFL'] <= 440.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 3'
		elif row['TOEFL'] >= 441.0 and row['TOEFL'] <= 460.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 4'
		elif row['TOEFL'] >= 461.0 and row['TOEFL'] <= 480.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 5'
		elif row['TOEFL'] >= 481.0 and row['TOEFL'] <= 500.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 6'
		elif row['TOEFL'] >= 501.0 and row['TOEFL'] <= 520.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 7'
		elif row['TOEFL'] >= 521.0 and row['TOEFL'] <= 540.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 8'
		elif row['TOEFL'] >= 541.0 and row['TOEFL'] <= 560.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 9'
		elif row['TOEFL'] >= 561.0 and row['TOEFL'] <= 580.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 10'
		elif row['TOEFL'] >= 581.0 and row['TOEFL'] <= 600.0:
			cleaning_mhs.loc[index, 'R. TOEFL'] = 'RANGE 11'

		#LAMA STUDI
		if '3 Th' in row['LAMA STUDI']:
			cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TEPAT'
		
		# elif '4 Th,0 Bln' in row['LAMA STUDI']:
		# 	cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TEPAT'
		# elif '4 Th, 0 Bln' in row['LAMA STUDI']:
		# 	cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TEPAT'	
		
		# elif '4 Th,5 Bln' in row['LAMA STUDI']:
		# 	cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TEPAT'
		# elif '4 Th, 5 Bln' in row['LAMA STUDI']:
		# 	cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TEPAT'
		
		else:
			cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TIDAK TEPAT'

	st.write("***Data Selection and Transformation***")	
	cleaning_mhs

	st.write("***Data Transformation***")
	transformasi_mhs = cleaning_mhs[['ASAL SEKOLAH', 'PROVINSI', 'KUANT. MATE', 'KUANT. IPK', 'R. TOEFL', 'STATUS KELULUSAN']]

	for index, row in transformasi_mhs.iterrows():
		# Wilayah 1 = Maluku Utara, Kalimantan Tengah
		# Wilayah 2 = Bali, Banten, Diy, Jakarta, Jambi, Jawa barat, Jawa tengah, 
		# 			Jawa Timur, Kalbar, Kep. Bangka, Aceh, NTB, Sulbar, Sulsel, Sulut, Riau, sumbar, Lampung, NTT, Sulteng, Kalsel, Bengkulu, Sumsel, Gorontalo, Sulteng, Sumut
		# Wilayah 3 = Papua, Maluku, Kalimantan Timur, Papua
		
		#PROVINSI
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
		
		# RATA IPK
		if row['KUANT. IPK'] == "ISTIMEWA":
			transformasi_mhs.loc[index, 'KUANT. IPK'] = 4
		elif row['KUANT. IPK'] == "BAIK":
			transformasi_mhs.loc[index, 'KUANT. IPK'] = 3
		elif row['KUANT. IPK'] == "CUKUP":
			transformasi_mhs.loc[index, 'KUANT. IPK'] = 2
		elif row['KUANT. IPK'] == "KURANG":
			transformasi_mhs.loc[index, 'KUANT. IPK'] = 1
		
		#TOEFL
		if row['R. TOEFL'] == "RANGE 11":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 11
		if row['R. TOEFL'] == "RANGE 10":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 10
		if row['R. TOEFL'] == "RANGE 9":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 9
		if row['R. TOEFL'] == "RANGE 8":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 8
		if row['R. TOEFL'] == "RANGE 7":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 7
		if row['R. TOEFL'] == "RANGE 6":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 6
		if row['R. TOEFL'] == "RANGE 5":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 5
		if row['R. TOEFL'] == "RANGE 4":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 4
		if row['R. TOEFL'] == "RANGE 3":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 3
		if row['R. TOEFL'] == "RANGE 2":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 2
		if row['R. TOEFL'] == "RANGE 1":
			transformasi_mhs.loc[index, 'R. TOEFL'] = 1

		#LAMA STUDI
		# if row['STATUS KELULUSAN'] == "TEPAT":
		# 	transformasi_mhs.loc[index, 'STATUS KELULUSAN'] = 0
		# else:
		# 	transformasi_mhs.loc[index, 'STATUS KELULUSAN'] = 1

	transformasi_mhs

	# temp_arr = transformasi_mhs[['USIA MASUK', 'PROVINSI', 'KUANT. MATE', 'KUANT. IPK', 'R. TOEFL', 'STATUS KELULUSAN']]
	# st.write("***Array***")
	# arr = temp_arr.to_numpy()
	# arr

	model = GaussianNB()
	st.write("***Data Training dan Testing***")
	x = transformasi_mhs[['ASAL SEKOLAH', 'PROVINSI', 'KUANT. MATE', 'KUANT. IPK', 'R. TOEFL']]
	x

	st.write("***Data Target***")
	y = transformasi_mhs['STATUS KELULUSAN']
	y
	y.shape

	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = split_tt, random_state = 1230) # 52019, 1230
	nbtrain = model.fit(x_train, y_train)

	st.markdown('***DATA TRAINING : ***')
	x_train
	x_train.shape

	st.markdown('***TARGET TRAINING : ***')
	y_train
	y_train.shape

	st.markdown('***DATA TESTING : ***')
	x_test
	x_test.shape

	st.markdown('***TARGET TESTING : ***')
	y_test
	y_test.shape

	y_pred = nbtrain.predict(x_test)
	st.write("***Data Prediksi***")
	y_pred
	y_pred.shape

	st.write("***Data Porbabilitas Prediksi***")
	predic_prob = nbtrain.predict_proba(x_test)
	predic_prob

	# Confusion matrix
	st.write("***Confusion Matrix***")
	conf_matr = confusion_matrix(y_test, y_pred)
	conf_matr
	df_confusion = pd.crosstab(y_test, y_pred)
	df_confusion

	report = classification_report(y_test, y_pred, target_names=['TP', 'TTP'])
	st.text(report)
	
	st.markdown('**HASIL PREDIKSI MAHASISWA NIM '+nim +' AKAN LULUS **')
	st.markdown('**DALAM JANGKA WAKTU :**')

	prediksi = model.predict([[asalSekolah,prov,rata_matematika,ipk,toefl]])
	st.markdown(prediksi)

	st.write("***PROBABILITAS PREDIKSI***")
	prediksi_prob = nbtrain.predict_proba([[asalSekolah,prov,rata_matematika,ipk,toefl]])
	prediksi_prob


else:
	st.write('UPLOAD FILE TERLEBIH DAHULU')