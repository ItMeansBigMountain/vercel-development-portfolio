import matplotlib.pyplot as plt


#PIE CHART FUNCTION!

# ( (tuple with strings), [array] )
def pieChart(labels, sizes,):
    explode = (0, 0, 0, 0) #explode should have as many items as labels / sizes
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
# pieChart( ("affan" , "larry"), [9,8] )




#BAR CHART FUNCTION

         #  ([array] , [array] , string , string , string, string)
def bar_chart(x , y , X_label , Y_label, Title , color_input):

    plt.style.use('ggplot')

    # x = []
    # y = []

    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color= color_input ) #STR ex: "green"
    plt.xlabel(X_label)
    plt.ylabel(Y_label)
    plt.title(Title)
    plt.xticks(x_pos, x)
    plt.xticks(rotation=90)
    plt.show()
# bar_chart([0,1,2,3] , [9,8,7,6] , "x" , "y" , "random", "blue")


