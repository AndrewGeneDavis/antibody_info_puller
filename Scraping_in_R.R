
#single site test/practice/tuning
{
  site_url <- "https://www.ptglab.com/products/N-cadherin-Antibody-22018-1-AP.htm"
  
  antibody1 <- readLines(con = site_url)
  
  antibody1.title <- antibody1[grep("\"product-title\"", antibody1)[1]+1]
  antibody1.title <- sub(".*>(.+)<.*", "\\1", antibody1.title)
  antibody1.host_and_isotype <- antibody1[grep("Isotype</strong", antibody1)[1]+1]
  antibody1.host <- sub(".*>(.+) /.*", "\\1", antibody1.host_and_isotype)
  antibody1.isotype <- sub(".*/ (.+)<.*", "\\1", antibody1.host_and_isotype)
  antibody1.reactivity <- antibody1[grep("Reactivity</strong", antibody1)[1]+1]
  antibody1.reactivity <- sub(".*?>(.+)</.*", "\\1", antibody1.reactivity)
  antibody1.clonality <- antibody1[grep("clonal", antibody1)[1]]
  antibody1.clonality <- sub(".*(....clonal).*", "\\1", antibody1.clonality)
  if(antibody1.clonality == "Polyclonal" || antibody1.clonality == "polyclonal"){
    antibody1.clonality <- "pAb"
  }else if(antibody1.clonality == "Monoclonal" || antibody1.clonality == "monoclonal"){
    antibody1.clonality <- "mAb"
  }

  antibodies <- data.frame(name = c(antibody1.title), reactivity = antibody1.reactivity, host = antibody1.host, type = antibody1.clonality, isotype = antibody1.isotype)
  antibodies <- rbind(antibodies, antibodies)
  antibodies[9,1] <- "next ab"
  antibodies[9,2] <- "reactive"
  #rm(list = c("antibody1", "antibody1.clonality", "antibody1.host", "antibody1.host_and_isotype", "antibody1.isotype", "antibody1.reactivity", "antibody1.title", "site_url", "url"))
}

library(RCurl)

url <- "ftp://www.ptglab.com/products/*Antibody-12530-1-AP.htm"
antibody_test <- readLines(url)


# Test run on 3 sites; it works, just plug them all in and get the data
{
  sitelist <- c("https://www.ptglab.com/products/N-cadherin-Antibody-22018-1-AP.htm", "https://www.ptglab.com/Products/BTG2-Antibody-22339-1-AP.htm", "https://www.ptglab.com/products/FMOD-Antibody-13281-1-AP.htm", "https://www.ptglab.com/products/PLEKHO1-Antibody-24883-1-AP.htm")
  
  for(i in 1:length(sitelist)){
    antibody <- readLines(con = sitelist[i])
    antibody.title <- antibody[grep("\"product-title\"", antibody)[1]+1]
    antibody.title <- sub(".*>(.+?)<.*", "\\1", antibody.title)
    antibody.host_and_isotype <- antibody[grep("Isotype</strong", antibody)[1]+1]
    antibody.host <- sub(".*>(.+?) /.*", "\\1", antibody.host_and_isotype)
    antibody.isotype <- sub(".*/ (.+?)<.*", "\\1", antibody.host_and_isotype)
    antibody.reactivity <- antibody[grep("Reactivity</strong", antibody)[1]+1]
    antibody.reactivity <- sub(".*>(.+?)</.*", "\\1", antibody.reactivity)
    antibody.clonality <- antibody[grep("clonal", antibody)[1]]
    antibody.clonality <- sub(".*(....clonal).*", "\\1", antibody.clonality)
    if(antibody.clonality == "Polyclonal" || antibody.clonality == "polyclonal"){
      antibody.clonality <- "pAb"
    }else if(antibody.clonality == "Monoclonal" || antibody.clonality == "monoclonal"){
      antibody.clonality <- "mAb"
    }
    if(i == 1){
      antibodies <- data.frame(name = c(antibody.title), reactivity = antibody.reactivity, host = antibody.host, type = antibody.clonality, isotype = antibody.isotype)
    }else if(i != 1){
      antibodies <- rbind(antibodies, data.frame(name = c(antibody.title), reactivity = antibody.reactivity, host = antibody.host, type = antibody.clonality, isotype = antibody.isotype))
    }
  }
  antibodies
  write.csv(antibodies, "ptg_antibodies_list.csv")
  rm(list=c("antibodies", "antibody", "antibody.clonality", "antibody.host", "antibody.host_and_isotype", "antibody.isotype", "antibody.reactivity", "antibody.title", "i", "sitelist"))
}

# apparently some of the lines are ridiculously long on these web pages (over 10k chars)
{
  str(antibody1)
  strings_lengths <- c()
  for(i in 1:length(antibody1)){
    strings_lengths <- c(strings_lengths, nchar(antibody1[i]))
  }
  max(strings_lengths)
  plot(strings_lengths)
}
