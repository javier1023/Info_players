library(readxl)
datos<- read.csv("EXPORT_DE_TABLEAU.csv",sep=';')
paises=levels(factor(datos$Pais.nacimiento))


#Aquí hacemos el data frame con el valor de la media de 'ELO/EDAD' = Valor de mercado generado de cada país
dataf=data.frame()
cont=1

  
for (i in paises[-1]) {
  datos_p<-datos[which(datos$Pais.nacimiento==i),]
  media=0
  for(j in 1:(nrow(datos_p))) {
    a=datos_p[j,"ELO.Edad"]
    if (is.na(a)==TRUE){}
    else {media=media+a}
  }
  dataf[cont,'Pais']=i
  dataf[cont,'Media']=format(round((media/nrow(datos_p)), 2), nsmall = 2)
  
  cont=cont+1
}
  
write.csv(dataf,'Base_paises_mediaELO-VM2.csv')

#Aquí hacemos el data frame con el valor de la media de valor de mercado generado de cada país

dataf2=data.frame()
cont=1


for (i in paises[-1]) {
  datos_p<-datos[which(datos$Pais.nacimiento==i),]
  media=0
  for(j in 1:(nrow(datos_p))) {
    a=datos_p[j,"Valor.de.mercado"]
    if (is.na(a)==TRUE){}
    else {media=media+a}
  }
  dataf2[cont,'Pais']=i
  dataf2[cont,'Media']=format(round((media/nrow(datos_p)), 2), nsmall = 2)
  
  cont=cont+1
}

write.csv(dataf2,'Base_paises_media_valor_mercado.csv')
