library(shiny)
library(shinydashboard)
library(plotly)
library(dplyr)
library(tidyr)
library(ggplot2)

years <- 2010:2023


# Define UI
ui <- dashboardPage(
  dashboardHeader(title = "Spurious Ireland"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
      menuItem("About", tabName = "about", icon = icon("info-circle"))
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(
        tabName = "dashboard",
        fluidRow(
          box(
            title = "Select Correlation", width = 12, status = "primary",
            selectInput("correlation", "Choose a Spurious Correlation:",
                        choices = c("Potato Yield vs. Net Migration" = "potato_migration",
                                    "Marriages vs. GDP Growth Rate" = "marriages_gdp"),
                        selected = "potato_migration")
          )
        ),
        fluidRow(
          box(
            title = "Time Period", width = 12, status = "info",
            sliderInput("year_range", "Select Years:",
                        min = min(years), max = max(years),
                        value = c(min(years), max(years)),
                        step = 1, sep = "")
          )
        ),
        fluidRow(
          box(
            title = "Spurious Correlation Visualization", width = 12, status = "warning",
            plotlyOutput("correlationPlot", height = "500px")
          )
        ),
        fluidRow(
          box(
            title = "Humorous Explanation", width = 12, status = "danger",
            htmlOutput("explanationText")
          )
        )
      ),
      tabItem(
        tabName = "about",
        fluidRow(
          box(
            title = "About This Dashboard", width = 12, status = "primary",
            h3("Correlation ≠ Causation: A Fun Exploration"),
            p("This dashboard demonstrates spurious correlations - statistical relationships between variables that have no causal connection."),
            p("Just because two trends appear similar doesn't mean one causes the other!"),
            p("This is a humorous demonstration of how statistics can be misleading when not properly interpreted."),
            br(),
            h4("How to use this dashboard:"),
            tags$ul(
              tags$li("Select a correlation from the dropdown menu"),
              tags$li("Adjust the time period using the slider"),
              tags$li("Observe how the correlation coefficient changes"),
              tags$li("Enjoy the humorous 'explanations' of these meaningless relationships")
            ),
            br(),
            p("Created with R, Shiny, and real data from the Central Statistics Office of Ireland.")
          )
        )
      )
    )
  )
)

# Define server logic
server <- function(input, output) {
  
  # Filtered dataset based on year range
  filtered_data <- reactive({
    all_data %>%
      filter(Year >= input$year_range[1] & Year <= input$year_range[2])
  })
  
  # Calculate correlation coefficients
  correlation_coef <- reactive({
    fd <- filtered_data()
    
    if(input$correlation == "potato_migration") {
      return(round(cor(fd$`Crop Production`, fd$`Net migration`), 2))
    } else {
      return(round(cor(fd$Marriages, fd$GDP_Growth_Rate), 2))
    }
  })
  
  # Generate plot
  output$correlationPlot <- renderPlotly({
    fd <- filtered_data()
    
    if(input$correlation == "potato_migration") {
      # Create potato yield vs migration plot
      p <- plot_ly() %>%
        add_lines(x = ~fd$Year, y = ~fd$`Crop Production`, 
                  name = "Potato Yield (tonnes)", 
                  line = list(color = "#8B4513", width = 3),
                  yaxis = "y1") %>%
        add_lines(x = ~fd$Year, y = ~fd$`Net migration`, 
                  name = "Net Migration (thousands)", 
                  line = list(color = "#2E8B57", width = 3),
                  yaxis = "y2") %>%
        layout(title = "The Curious Relationship Between Potato Yields and Migration",
               xaxis = list(title = "Year"),
               yaxis = list(title = "Potato Yield (tonnes)", 
                            side = "left"),
               yaxis2 = list(title = "Net Migration (thousands)", 
                             side = "right",
                             overlaying = "y"),
               legend = list(orientation = "h", y = 1.1))
    } else {
      # Create marriages vs GDP plot
      p <- plot_ly() %>%
        add_lines(x = ~fd$Year, y = ~fd$Marriages, 
                  name = "Number of Marriages", 
                  line = list(color = "#FF69B4", width = 3),
                  yaxis = "y1") %>%
        add_bars(x = ~fd$Year, y = ~fd$GDP_Growth_Rate, 
                 name = "GDP Growth Rate (%)", 
                 marker = list(color = "#4682B4", opacity = 0.7),
                 yaxis = "y2") %>%
        layout(title = "Marriage Rates and Economic Prosperity: A Love Story?",
               xaxis = list(title = "Year"),
               yaxis = list(title = "Number of Marriages", 
                            side = "left"),
               yaxis2 = list(title = "GDP Growth Rate (%)", 
                             side = "right",
                             overlaying = "y"),
               legend = list(orientation = "h", y = 1.1))
    }
    
    return(p)
  })
  
  # Generate explanation text
  output$explanationText <- renderUI({
    corr <- correlation_coef()
    
    if(input$correlation == "potato_migration") {
      HTML(paste0(
        "<h3 style='text-align:center; color:#4B0082;'>Potato Yields & Migration: r = ", corr, "</h3>",
        "<p>Who would have thought? As Ireland's potato yields fluctuate, so too does the migration pattern! ",
        "With a correlation coefficient of ", corr, ", one might humorously suggest that Irish people are ",
        "making life decisions based on the health of the potato crop. Perhaps the collective memory of the ",
        "Great Famine still influences the national psyche? Or maybe people just really like potatoes?</p>",
        "<p><em>Of course, this is purely coincidental. Migration is influenced by economic opportunities, housing costs, ",
        "and global conditions, while potato yields depend on agricultural practices, weather, and growing conditions.</em></p>"
      ))
    } else {
      HTML(paste0(
        "<h3 style='text-align:center; color:#4B0082;'>Marriages & GDP Growth: r = ", corr, "</h3>",
        "<p>With a correlation coefficient of ", corr, ", one might be tempted to believe that economic prosperity ",
        "drives people to tie the knot! Or perhaps all those wedding expenses are boosting Ireland's GDP? ",
        "The wedding industry must be more powerful than we thought!</p>",
        "<p><em>In reality, marriage rates are influenced by social trends, age demographics, and changing attitudes toward ",
        "relationships, while GDP growth depends on countless economic factors including global trade, investment, ",
        "productivity, and government policies.</em></p>"
      ))
    }
  })
}

# Run the application
shinyApp(ui = ui, server = server)