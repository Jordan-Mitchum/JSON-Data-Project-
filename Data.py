from flask import Flask, request, Markup, render_template, flash
import json

app = Flask(__name__)

@app.route('/')   
def render_home():
    return render_template('home.html')
    
@app.route('/about')
def render_about():
    return render_template('about.html')

@app.route('/Likes')
def render_Likes():
    return render_template('likes.html')

@app.route('/popularity')
def render_popularity():
    return render_template('mvp.html', options = options())
    
def options():
    with open('super_bowl_ads.json') as Ads:
        Ads_data = json.load(Ads) 
#the drop down menu and also gets year
    year = []
    for y in Ads_data:
        if y['Year'] not in year:
           year.append(y['Year'])
           
    a = ""
    for y in year:
        a = a + Markup('<option value = "'+ str(y) + '">'+ str(y) + '</option>')
    return a
        
    
@app.route('/popularity_response')
def render_popularity_response():
    with open('super_bowl_ads.json') as Ads:
        Ads_data = json.load(Ads) 
#gets year for html drop down menu
    Year = ""
    if 'year' in request.args:
        Year = request.args['year']
        brand = {}
        for a in Ads_data: 
            if str(a['Year']) == Year:
                if a['Brand'] in brand:
                    brand[a['Brand']] = brand[a['Brand']] + a['Data']['Viewership']['Views']
                else:
                    brand[a['Brand']] = a['Data']['Viewership']['Views']
#Gets the most viewed brand 
    print(brand)                  
    MostViewed = "Budweiser"
    for r in brand:
        if brand[r] > brand[MostViewed]:
            MostViewed = r
    return render_template('mvp_display.html', Year = Year, mostViewed = MostViewed, Views=brand[MostViewed], options = options())
    
@app.route('/category')
def render_category():
#Gets the year 
    year = []
    with open('super_bowl_ads.json') as Ads:
        Ads_data = json.load(Ads) 
    for y in Ads_data:
        if y['Year'] not in year:
           year.append(y['Year'])
    a = ""
    for y in year:
        a = a + Markup('<option value = "'+ str(y) + '">'+ str(y) + '</option>')
    return render_template('category.html', options = a)

@app.route('/category_response')
def render_category_response():
    with open('advertisements.json') as Ads:
        Ads_data = json.load(Ads) 
        
        
    category = most_pop_cat(request.args['year'],Ads_data)
    return render_template('category_display.html', Year = request.args['year'], mostUsed = category[0], used = category[1], options = options())

def most_pop_cat(year, data):
#Finds the most populay category based on the users choice of year
    cat = {"funny":0, "show_product_quickly":0, "patriotic":0, "celebrity":0,"danger":0,"animals":0,"use_sex":0}
    for ad in data:
        if str(ad['year']) == year:
        
            if ad["funny"] == "TRUE":
                cat['funny'] = cat['funny'] + 1
                
            if ad["show_product_quickly"] == "TRUE":
                cat['show_product_quickly'] = cat['show_product_quickly'] + 1

            if ad["patriotic"] == "TRUE":
                cat['patriotic'] = cat['patriotic'] + 1

            if ad["celebrity"] == "TRUE":
                cat['celebrity'] = cat['celebrity'] + 1
             
            if ad["danger"] == "TRUE":
                cat['danger'] = cat['danger'] + 1
                
            if ad["animals"] == "TRUE":
                cat['animals'] = cat['animals'] + 1
                
            if ad["use_sex"] == "TRUE":
                cat['use_sex'] = cat['use_sex'] + 1
                
    MyCat={'funny': "Comedy",
    'show_product_quickly': "Showing the Product",
    'patriotic': "Patriotic", 
    'celebrity':"Celebrity", 
    'danger': "Danger",
    'animals': "Animals",
    'use_sex': "Sexual appeal"}
    
#finds the highest nuber for category used
    print(cat)
    category = []
    highest = 0
    for c in cat:
        if cat[c] == highest:
            category.append(c)
            
        if cat[c] > highest:
            highest = cat[c]
            category = []
            category.append(c)
        
    print(highest)
    print(category)
    CT = ""
    for c in category:
       CT = CT + Markup(MyCat[c] + ",")
    return [CT[:-1], highest]
    
if __name__ == '__main__':
    app.run(debug=True)
    
  # for c in ad['Data']['Content']:
                #if ad['Data']['Content'][c] == True:  
                   # if c in cat:
                      #  cat[c] = cat[c] + 1
                  #  else:
                      #  cat[c] = 1