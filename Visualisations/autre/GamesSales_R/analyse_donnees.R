# Toutes les library utilisées
library(questionr)
library(ggplot2)
library(scales)
library(ggmosaic)
library(viridis)
library(dplyr)
library(tidyr)
library(patchwork)

rm(list = ls())


#-------------
#-----------------
data <- read.csv("vgsales.csv", header = TRUE)
class(data)
head(data)

summary(data)
colnames(data)

# Regardons le nombre d'occurence de chaque genre de jeux vidéo
genre<-table(data$Genre)
head(genre)

barplot(genre)


# Regardons les consoles sur lesqueles sont sortis les jeux
consol<-table(data$Platform)
consol<-consol[consol>50]
head(consol)

barplot(consol)


# Regardons le nombre d'occurence de chaque année
year<-table(data$Year)
head(year)

barplot(year)


# Les publisher avec le plus de jeux vidéo créé
publisher_df<-table(data$Publisher)
head(publisher_df)
nrow(publisher_df)
publisher_df<-publisher_df[publisher_df>50]

barplot(publisher_df)


#-------------
#-----------------
# On modifie le type des données des colonnes Sales
data$NA_Sales <- as.numeric(gsub(",", ".", gsub(" €", "", data$NA_Sales)))
data$JP_Sales <- as.numeric(gsub(",", ".", gsub(" €", "", data$JP_Sales)))
data$EU_Sales <- as.numeric(gsub(",", ".", gsub(" €", "", data$EU_Sales)))
data$Other_Sales <- as.numeric(gsub(",", ".", gsub(" €", "", data$Other_Sales)))
data$Global_Sales <- as.numeric(gsub(",", ".", gsub(" €", "", data$Global_Sales)))


# Data frame pour les comparaisons des ventes de chaque region proposer
ventes_df <- data.frame(
  Region = rep(c("NA", "EU", "JP", "Other", "Global"), each = nrow(data)),
  Sales = c(
    data$NA_Sales,
    data$EU_Sales,
    data$JP_Sales,
    data$Other_Sales,
    data$Global_Sales
  )
)
head(ventes_df)

ggplot(ventes_df, aes(x = Region, y = Sales, fill = Region)) +
  geom_boxplot() +
  scale_y_log10(labels = label_number())+
  theme_minimal()


#-------------
#-----------------
# Graphique genre/publisher
genre_publicher_df<-table(data$Genre,data$Publisher)
genre_publicher_df<-as.data.frame(genre_publicher_df)
colnames(genre_publicher_df) <- c("Genre", "Publisher", "Effectif")
head(genre_publicher_df)

# On ajoute un filtre aux données
genre_publicher_df <- genre_publicher_df[genre_publicher_df$Effectif > 10, ]
head(genre_publicher_df)

ggplot(genre_publicher_df, aes(x = Publisher, y = Effectif, fill = Genre)) +
  geom_col() +
  labs(
    y = "Effectif",
    x = "",
    fill = "Genre"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 6),
    axis.text.y = element_text(size = 10),
    legend.title = element_text(size = 16, margin = margin(b = 10)),
    legend.text = element_text(size = 10),
    legend.spacing = unit(10, "pt")
  )

# On affiche seulement les 20 plus grands publisher de jeux vidéo
publisher_list <- sort(publisher_df,T)
publisher_list <- publisher_list[1:20]
publisher_list <- as.data.frame(publisher_list)
colnames(publisher_list)<- c("Publisher", "Effectif")
publisher_list <- as.array(publisher_list[,"Publisher"])
publisher_list <- as.character(publisher_list)
publisher_list


#-------------
#-----------------
# On filtre le tout
genre_publicher_df$Publisher <- as.character(genre_publicher_df$Publisher)
genre_publicher_df <- genre_publicher_df[genre_publicher_df$Publisher %in% publisher_list,]
genre_publicher_df

ggplot(genre_publicher_df, aes(x = Publisher, y = Effectif, fill = Genre)) +
  geom_col() +
  labs(
    y = "Effectif",
    x = "",
    fill = "Genre"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1, size = 6),
    axis.text.y = element_text(size = 10),
    legend.title = element_text(size = 16, margin = margin(b = 10)),
    legend.text = element_text(size = 10),
    legend.spacing = unit(10, "pt")
  )


#-------------
#-----------------
# Meme chose mais en pourcentage : diagramme mosaïque
ggplot(data = genre_publicher_df) +
  geom_mosaic(aes(x = product(Publisher), fill = Genre)) +
  scale_fill_viridis(discrete = TRUE,  direction=-1) +
  labs(title = "",
       x = "",
       y = "Proportion") +
  scale_y_continuous(labels = scales::percent) +
  labs(fill = "Satisfaction Travail")+
  theme(axis.title.y = element_text(margin = margin(r = 20),size=10),
        axis.title.x = element_text(margin = margin(t=20),size=10),
        axis.text.y = element_text( size = 10),
        axis.text.x = element_text( size = 10,angle = 45, hjust = 1),
        legend.title = element_text(size = 10,margin = margin(b = 20)),
        legend.text = element_text(size = 10),
        legend.spacing = unit(15, "pt")
  )


#-------------
#-----------------
# Représentations de toutes les données
# Seconde csv : jeuxsteam.csv
data_f <- read.csv2("jeuxsteam.csv", header = TRUE)
class(data_f)
head(data_f)

colnames(data_f)


#-------------
#-----------------
# Fusion des csv
# Data frame sans perte d'information mais avec doublons
final_df<-merge.data.frame(data, data_f, by = "name")
final_df["Total_ratings"]<-final_df$positive_ratings+final_df$negative_ratings
final_df["Proportion_ratings_pos"]<-final_df$positive_ratings/final_df$Total_ratings
final_df["Proportion_ratings_neg"]<-final_df$negative_ratings/final_df$Total_ratings
head(final_df)
colnames(final_df)
nrow(final_df)


# Data frame sans doublons
final <- final_df[!duplicated(final_df$name), ]
final$price <- as.numeric(final$price)



#-------------
#-----------------
# Données finales
# Analyse simple
final_genre <- as.data.frame(final %>%
                               separate_rows(genres, sep = ";"))
final_genre[final_genre==0] <- 0.01

ggplot(final_genre, aes(x = genres, y = Global_Sales)) +
  geom_point(alpha = 0.5) +
  scale_y_log10() +
  theme_minimal() +
  labs(
    x = "Genre",
    y = "Ventes globales",
  )

# Nombre de genre
tab_genre <- table(final_genre$genres)
barplot(tab_genre,
        las = 2,
        col = "lightblue",
        main = "Nombre d'occurrences par genre")




# Modification des valeur 0 par 0.01 pour les graphes à échelle logaritmique
final[final==0] <- 0.01
head(final)
colnames(final)
nrow(final)

#--------------
#Graphique nombre d'avis total par nombre de vente par pays
list_zones<-c("NA_Sales","EU_Sales","JP_Sales","Other_Sales")

plots <- lapply(list_zones, function(zone) {
  ggplot(final, aes(x = Total_ratings, y = .data[[zone]])) +
    geom_point(alpha = 0.5) +
    scale_x_log10() +
    scale_y_log10() +
    theme_minimal() +
    labs(
      title = zone,
      x = "Nombre d’avis total",
      y = "Ventes"
    )
})

wrap_plots(plots, ncol = 2)


#--------------
# Graphique nombre d'avis total par nombre de vente globale
# avec une droite de régréssion linéaire
ggplot(final, aes(x = Global_Sales, y = Total_ratings)) +
  geom_point(alpha = 0.5) +
  scale_x_log10() +
  scale_y_log10() +
  theme_minimal() +
  geom_smooth(
    method = "lm",
    formula = y ~ x,
    se = FALSE,
    color = "red"
  ) +
  theme_minimal() +
  labs(
    x = "Ventes globales",
    y = "Nombre d’avis total",
  )


#--------------
# Calcul du coefficient de corrélation de Pearson
correlation <- function(a, b){
  coeff_cor <- cor(a, b, method = "pearson")
  print(coeff_cor)
  if (abs(coeff_cor) < 0.5){
    print("Le coefficient de correlation de Pearson est inférieur à 0,5.")
  } else {
    print("Le coefficient de correlation de Pearson est supérieur à 0,5.")
  }
}
correlation(final$Total_ratings, final$Global_Sales)


#--------------
# Graphique nombre avis negatifs en fonction du prix
ggplot(final, aes(x = price, y = Global_Sales)) +
  geom_point(alpha = 0.5) +
  scale_y_log10() +
  theme_minimal() +
  geom_smooth(
    method = "lm",
    formula = y ~ x,
    se = FALSE,
    color = "red"
  ) +
  labs(
    x = "Prix",
    y = "Vente globale",
    title = "Vente globale par prix"
  )
correlation(final$price, final$Global_Sales)

#--------------
# Graphe nombre d'avis positifs par nombre d'avis negatifs
ggplot(final, aes(x = negative_ratings, y = positive_ratings)) +
  geom_point(alpha = 0.5) +
  scale_x_log10() +
  scale_y_log10() +
  theme_minimal() +
  geom_smooth(
    method = "lm",
    formula = y ~ x,
    se = FALSE,
    color = "red"
  ) +
  labs(
    x = "Prix",
    y = "Vente globale",
    title = "Vente globale par prix"
  )
correlation(final$negative_ratings, final$positive_ratings)


#--------------
# Graphe nombre de jeux par plateforme
table_platform <- table(final_df$Platform)
table_platform <- table_platform[table_platform > 40]
table_platform <- sort(table_platform, T)
barplot(table_platform)


#--------------
# Graphe plateforme par vente globale
ggplot(final_df, aes(x = Platform, y = Global_Sales)) +
  geom_boxplot(fill = "yellow", color = "black") +
  scale_y_log10() +
  labs(
    title = "Boxplot de vente globale par plateforme",
    x = "Plateforme",
    y = "Vente globale"
  ) +
  theme_minimal()




#-------------
#-----------------
# Lien possible entre les variables price et average_playtime
ggplot(final, aes(x = price, y = average_playtime)) +
  geom_point(alpha = 0.5) +
  scale_y_log10() +
  theme_minimal() +
  labs(
    x = "price",
    y = "average_playtime",
    title = "Vente globale par prix"
  )
correlation(final$price, final$average_playtime)




#-------------
#-----------------
# Sans lien : les variables Global_Sales et average_playtime
ggplot(final, aes(x = Global_Sales, y = average_playtime)) +
  geom_point(alpha = 0.5) +
  scale_x_log10() +
  scale_y_log10() +
  theme_minimal() +
  labs(
    x = "price",
    y = "average_playtime",
    title = "Vente globale par prix"
  )
correlation(final$price, final$average_playtime)






#-------------
#-----------------
# Data frame complet en séparant les colonnes à réponses multiples
# Data frame séparation variable plateforms
final_df_separe <- final_df %>%
  separate_rows(platforms, sep = ";")

final_df_separe

barplot(final_df_separe$platforms)


#-------------
#-----------------
# Graphe nombre de jeu par système d'exploitation
table_plateform <- table(final_df$platforms)
table_plateform
table_plateform["windows"] <- table_plateform["windows"] + table_plateform["windows;linux"] +
  table_plateform["windows;mac;linux"] + table_plateform["windows;mac"]
table_plateform["mac"] <- table_plateform["windows;mac"] + table_plateform["windows;mac;linux"]
table_plateform["linux"] <- table_plateform["windows;linux"] + table_plateform["windows;mac;linux"]
table_plateform <- table_plateform[c("windows", "mac", "linux")]

barplot(as.numeric(table_plateform),
        names.arg = names(table_plateform),
        las = 2)

plateform_df <- final_df[!duplicated(final_df$name), ]
plateform_df <- as.data.frame(plateform_df %>%
                                separate_rows(platforms, sep = ";"))

ggplot(plateform_df, aes(x = platforms, y = Global_Sales)) +
  geom_point(alpha = 0.5) +
  scale_y_log10() +
  theme_minimal() +
  labs(
    x = "Système d'exploitation",
    y = "Vente globale",
    title = "Système d'exploitation par vente globale"
  )

# Graphe des ventes globals par nombre de système d'exploitation disponible
ggplot(plateform_df, aes(x = platforms, y = Global_Sales)) +
  geom_boxplot(fill = "yellow", color = "black") +
  scale_y_log10() +
  labs(
    title = "Vente global par nombre de système d'exploitation disponible",
    x = "Système d'exploitation",
    y = "Vente"
  ) +
  theme_minimal()

print("Au final pas vraiment de différence entre les différents pays et leur achat de jeux moyen")


#-------------
#-----------------
# Graphique nombre avis negatifs en fonction du prix
ggplot(final, aes(x = Proportion_ratings_pos, y = price)) +
  geom_point(alpha = 0.5) +
  theme_minimal() +
  labs(
    x = "Nombre d’avis negatifs",
    y = "Prix",
    color = "Type d’avis",
    title = "Avis negatifs par prix"
  )


#-------------
# Calcul du coefficient de corrélation de Pearson
coeff_cor <- cor(final$price, final$Global_Sales, method = "pearson")
coeff_cor
if (abs(coeff_cor) < 0.5){
  print("Le coefficient de correlation de Pearson est inférieur à 0,5.")
} else {
  print("Le coefficient de correlation de Pearson est supérieur à 0,5.")
}





#-------------
#-----------------
# Créer le data frame final
# Suppréssion des colonnes inutiles
df_final <- final_df
df_final$english <- as.logical(df_final$english)
df_final <- df_final %>%
  select(-Genre, -Publisher, -appid)
nrow(df_final)

# Créer des data frame sans perte d'information
# Dédoublement des lignes avec des énumérations dans les colonnes choisies
df_final_categ <- as.data.frame(df_final %>%
                                  separate_rows(categories, sep = ";"))
nrow(df_final_categ)

df_final_tags <- as.data.frame(df_final %>%
                                 separate_rows(steamspy_tags, sep = ";"))
nrow(df_final_tags)

df_final_genre <- as.data.frame(df_final %>%
                                  separate_rows(genres, sep = ";"))
nrow(df_final_tags)

df_final_platf <- as.data.frame(df_final %>%
                                  separate_rows(platforms, sep = ";"))
nrow(df_final_platf)

#-------------
# Graphes :
# Analyses univariés
# Occurrence des jeux sortis par année (nombre de jeu par années)
barplot(table(final$Year))
class(final$release_date)

final$release_date <- as.numeric(substr(final$release_date, 1, 4))
head(final$release_date)

df_counts <- final %>%
  count(Year, name = "effectif")

ggplot(df_counts, aes(x = Year, y = effectif)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_text(aes(label = effectif), vjust = -0.5, size = 5) +
  labs(title = "Effectifs par catégorie",
       x = "Catégorie",
       y = "Effectif") +
  theme_minimal()

#ou 

df_counts_2 <- final %>%
  count(release_date, name = "effectif")
head(final$release_date)

ggplot(df_counts_2, aes(x = release_date, y = effectif)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  geom_text(aes(label = effectif), vjust = -0.5, size = 5) +
  labs(title = "Effectifs par catégorie",
       x = "Catégorie",
       y = "Effectif") +
  theme_minimal()

# Occurrence des jeux par le nombre de personnes qui le possède
barplot(table(final$owners))

# Occurrence des jeux par le nombre de personnes qui le possède
barplot(table(final$required_age))

# Occurrence des jeux en anglais (nombre de jeu en anglais)
barplot(table(final$english))

# Occurrence des jeux par tranche de prix (nombre de jeu par tranche de prix)
final$price_cat <- cut(final$price,
                       breaks = quantile(final$price, probs = seq(0, 1, 0.25), na.rm = TRUE),
                       include.lowest = TRUE)
barplot(table(final$price_cat))

# Occurrence des jeux par tranche de temps de jeu (nombre de jeu par tranche de temps de jeu)
final$time_cat <- cut(final$average_playtime,
                      breaks = quantile(final$price, probs = seq(0, 1, 0.25), na.rm = TRUE),
                      include.lowest = TRUE)
barplot(table(final$time_cat))

# Occurrence des publishers
publisher_tab <- table(final$publisher)
publisher_tab <- publisher_tab[publisher_tab>=10]
barplot(publisher_tab)

# Occurrence des developers
dev_tab <- table(final$developer)
dev_tab <- dev_tab[dev_tab>=5]
barplot(dev_tab)

# Occurrence des différentes catégories (nombre de jeu par cathégorie)
barplot(table(df_final_categ$categories))

# Occurrence des différents genres (nombre de jeu par genre)
barplot(tab_genre, main = "Nombre d'occurrences par genre")

# Occurrence des différents tags (nombre de jeu par tag)
tab <- table(df_final_tags$steamspy_tags)
tab <- tab[tab > 50]
barplot(tab)

# Modification des valeurs pour les graphes à échelle logarithmique
df_final_categ[df_final_categ==0] <- 0.01
df_final_tags[df_final_tags==0] <- 0.01


#-------------
# Analyses bivariés
plots <- lapply(list_zones, function(zone) {
  ggplot(df_final_categ, aes(x = categories, y = .data[[zone]])) +
    geom_boxplot(fill = "yellow", color = "black") +
    scale_y_log10() +
    labs(
      title = zone,
      x = "Catégorie",
      y = "Vente"
    ) +
    theme_minimal()
})
wrap_plots(plots, ncol = 2)


#-------------
# Graphe catégories
df_final_categ$price <- as.numeric(df_final_categ$price)
df_categ_summary <- df_final_categ %>%
  group_by(categories) %>%
  summarise(
    prix_moyen = mean(price, na.rm = TRUE),
    prix_med = median(price, na.rm = TRUE),
    n_jeux = n()
  )

ggplot(df_categ_summary, aes(x = reorder(categories, prix_moyen), y = prix_moyen)) +
  geom_col(fill = "lightblue") +
  theme_minimal() +
  labs(
    x = "Catégorie",
    y = "Prix moyen",
    title = "Prix moyen par catégorie de jeux"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


ggplot(df_final_categ, aes(x = categories, y = Global_Sales)) +
  geom_boxplot() +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


#-------------
# Graphe tags
df_final_tags$price <- as.numeric(df_final_tags$price)
df_tags_summary <- df_final_tags %>%
  group_by(steamspy_tags) %>%
  summarise(
    prix_moyen = mean(price, na.rm = TRUE),
    prix_med = median(price, na.rm = TRUE),
    n_jeux = n()
  )

df_tags_summary <- df_tags_summary[df_tags_summary$n_jeux >= 30,]
nrow(df_tags_summary)

ggplot(df_tags_summary, aes(x = reorder(steamspy_tags, prix_moyen), y = prix_moyen)) +
  geom_col(fill = "lightblue") +
  theme_minimal() +
  labs(
    x = "Catégorie",
    y = "Prix moyen",
    title = "Prix moyen par catégorie de jeux"
  ) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


ggplot(df_final_categ, aes(x = categories, y = Global_Sales)) +
  geom_boxplot() +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))



#-------------
#-----------------
# Quelques testes statistiques
# Le khi deux d'indépendance (Monte Carlo)

khi <- function(a, b){
  table <- table(a, b)
  resultat_simule <- chisq.test(table, 
                                simulate.p.value = TRUE, 
                                B = 10000)
  
  if((resultat_simule$p.value) < 0.05){
    print(paste("Les variables sont dépendantes avec une p-value de", resultat_simule$p.value))
  } else {
    print(paste("Les variables sont indépendantes avec une p-value de", resultat_simule$p.value))
  }
}

khi(df_final_genre$genres, df_final_genre$publisher)
khi(df_final_genre$genres, df_final_genre$Year)
khi(df_final_categ$categories, df_final_categ$Year)


#------------
#---------------
# Data frame avec toute les données sur un seul et même jeu sur une seule et même ligne
df <- final_df[!duplicated(final_df$name), ]
df <- data.frame(df[,c("name","Rank","Year","publisher","achievements","release_date","Platform",
                       "required_age","positive_ratings","negative_ratings","price","average_playtime","median_playtime","owners",
                       "NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales")])
nrow(df)
head(df)
colnames(final)

# Liste des valeurs possibles de chaque variables concernées
nom_genre <- df_final_genre[!duplicated(df_final_genre$genres), ]
nom_genre <- nom_genre$genres
nom_genre

nom_tags <- df_final_tags[!duplicated(df_final_tags$steamspy_tags), ]
nom_tags <- nom_tags$steamspy_tags
nom_tags

nom_categ <- df_final_categ[!duplicated(df_final_categ$categories), ]
nom_categ <- nom_categ$categories
nom_categ

nom_platf <- df_final_platf[!duplicated(df_final_platf$platforms), ]
nom_platf <- nom_platf$platforms
nom_platf

# Ajout des données dans le df
for (nom in nom_genre) {
  jeux_avec_genre <- df_final_genre$name[df_final_genre$genres == nom]
  df[[paste0("genre_", nom)]] <- ifelse(df$name %in% jeux_avec_genre, 1, 0)
}

for (nom in nom_tags) {
  jeux_avec_tags <- df_final_tags$name[df_final_tags$genres == nom]
  df[[paste0("tag_", nom)]] <- ifelse(df$name %in% jeux_avec_tags, 1, 0)
}

for (nom in nom_categ) {
  jeux_avec_categ <- df_final_categ$name[df_final_categ$categories == nom]
  df[[paste0("cat_", nom)]] <- ifelse(df$name %in% jeux_avec_categ, 1, 0)
}

for (nom in nom_platf) {
  jeux_avec_platf <- df_final_platf$name[df_final_platf$platforms == nom]
  df[[paste0("platf_", nom)]] <- ifelse(df$name %in% jeux_avec_platf, 1, 0)
}


head(df)
colnames(df)











#-------------
#-----------------
# Création des csv avec dissosiation des différentes vavriables
csv_categ <- df_final_categ[,c("name","categories")]
csv_genre <- df_final_genre[,c("name","genres")]
csv_tags <- df_final_tags[,c("name","steamspy_tags")]
csv_tot <- df

# csv categ
tryCatch({
  write.csv(
    csv_categ,
    file = "categorie.csv",
    row.names = FALSE,
    fileEncoding = "UTF-8",
    na = ""
  )
  cat("Fichier 'categorie.csv' créé avec succès.\n")
}, error = function(e) {
  cat("Erreur lors de l'écriture du fichier :", e$message, "\n")
})

# csv genre
tryCatch({
  write.csv(
    csv_genre,
    file = "genre.csv",
    row.names = FALSE,
    fileEncoding = "UTF-8",
    na = ""
  )
  cat("Fichier 'genre.csv' créé avec succès.\n")
}, error = function(e) {
  cat("Erreur lors de l'écriture du fichier :", e$message, "\n")
})

# csv tags
tryCatch({
  write.csv(
    csv_tags,
    file = "tags.csv",
    row.names = FALSE,
    fileEncoding = "UTF-8",
    na = ""
  )
  cat("Fichier 'tags.csv' créé avec succès.\n")
}, error = function(e) {
  cat("Erreur lors de l'écriture du fichier :", e$message, "\n")
})

# csv total
tryCatch({
  write.csv(
    csv_tot,
    file = "total.csv",
    row.names = FALSE,
    fileEncoding = "UTF-8",
    na = ""
  )
  cat("Fichier 'total.csv' créé avec succès.\n")
}, error = function(e) {
  cat("Erreur lors de l'écriture du fichier :", e$message, "\n")
})


