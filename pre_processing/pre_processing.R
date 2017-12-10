standard_pub_2 = read.csv(file = "~/Box Sync/Yuchen_project/Truven_rising_stars/data_seperate_sheet/standard_pubs_2.csv", encoding = 'utf-8')
standard_pub_3 = standard_pub_2[,1:3]
write.csv(standard_pub_3, file = '~/Box Sync/Yuchen_project/Truven_rising_stars/data_seperate_sheet/standard_pubs_3.csv', sep = ",", fileEncoding = 'utf-8', row.names = FALSE)
 