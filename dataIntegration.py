import numpy as np
import streamlit as st
import pandas as pd
from openpyxl import load_workbook

def cleaningData(uploadedFile):
	st.write("***Data Mahasiswa***")
	wb = load_workbook(uploadedFile)
	sheet_ranges = wb["Sheet1"]

	datamhs = pd.DataFrame(sheet_ranges.values)
	datamhs = datamhs[datamhs != 0]

	st.write(datamhs)

	st.write("***Jumlah Data Awal***")
	st.write(datamhs.shape)
	jml_row = datamhs[0].count()

	cleaning_mhs = datamhs[1:jml_row][[1,2,3,4,5,6,7]]
	st.write("***Data Cleaning***")
	cleaning_mhs.columns = ['NIM', 'NAMA', 'ASAL SEKOLAH', 'PRODI', 'PROVINSI', 'RATA MATE', 'LAMA STUDI']

	# menghapus data noise
	cleaning_mhs = cleaning_mhs.dropna(axis=0, how='any')
	st.write(cleaning_mhs)

	st.write("***Jumlah Data Setelah Cleaning***")
	st.write(cleaning_mhs.shape)

	# mengubah tipe data dari object ke float
	cleaning_mhs['RATA MATE'] = cleaning_mhs['RATA MATE'].apply(str)
	cleaning_mhs['RATA MATE'] = cleaning_mhs['RATA MATE'].str.replace(',','.').apply(float)
	cleaning_mhs['LAMA STUDI'] = cleaning_mhs['LAMA STUDI'].apply(str)
	cleaning_mhs['LAMA STUDI'] = cleaning_mhs['LAMA STUDI'].str.replace(',','.').apply(float)

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

		#LAMA STUDI
		if row['LAMA STUDI'] >= 1461:
			cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TIDAK TEPAT'
		else:
			cleaning_mhs.loc[index, 'STATUS KELULUSAN'] = 'TEPAT'

	st.write("***Data Selection and Transformation***")	
	st.write(cleaning_mhs)

	st.write("***Data Transformation***")
	transformasi_mhs = cleaning_mhs[['PRODI', 'ASAL SEKOLAH',  'PROVINSI', 'KUANT. MATE', 'STATUS KELULUSAN']]

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

		#LAMA STUDI
		# if row['STATUS KELULUSAN'] == "TEPAT":
		# 	transformasi_mhs.loc[index, 'STATUS KELULUSAN'] = 0
		# else:
		# 	transformasi_mhs.loc[index, 'STATUS KELULUSAN'] = 1
	
	st.write (transformasi_mhs)
	return transformasi_mhs
