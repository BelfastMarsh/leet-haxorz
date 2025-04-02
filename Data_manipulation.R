#pull in data
library(csodata)
library(tidyverse)

content_list <- csodata::cso_get_toc()

pea15 <- csodata::cso_get_data("PEA15")
aqa04 <- csodata::cso_get_data("AQA04")
vsa01 <- csodata::cso_get_data("VSA01")
naq03 <- csodata::cso_get_data("NAQ03")
vsa44 <- csodata::cso_get_data("VSA44")

mig_data <- pea15 %>%
  filter(Component == "Net migration") %>%
  pivot_longer(cols = -c("STATISTIC", "Component"), names_to = "Year", values_to = "Value") %>%
  select(-STATISTIC) %>%
  rename(Statistic = Component)

potato_data <- aqa04 %>%
  pivot_longer(cols = -c("Statistic", "Type.of.Crop"), names_to = "Year", values_to = "Value") %>%
  filter(Statistic == "Crop Production" & Type.of.Crop == "Potatoes") %>%
  select(-Type.of.Crop)

bir_data <- vsa01 %>%
  pivot_longer(cols = -c("STATISTIC", "Sex"), names_to = "Year", values_to = "Value") %>%
  filter(Sex == "Both sexes") %>%
  select(-Sex) %>%
  rename(Statistic = STATISTIC)

marr_data <- vsa44 %>%
  filter(Form.of.Ceremony=="All ceremonies", Province.County.and.City=="State") %>%
  select(-c(Form.of.Ceremony, Province.County.and.City))

marr_data <- marr_data%>%
  pivot_longer(cols = -Statistic, names_to = "Year", values_to = "Value")

all_data <- rbind(mig_data, potato_data, bir_data, marr_data)

all_data <- all_data %>%
  pivot_wider(names_from = "Statistic", values_from = "Value")

all_data <- all_data %>%
  filter(Year >=2008)
