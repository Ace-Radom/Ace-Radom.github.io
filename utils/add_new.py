import os

from datetime import datetime

def get_templates() -> list[str]:
    templates = []
    for root , ds , fs in os.walk( "./template" ):
        for f in fs:
            templates.append( f[0:f.find( "." )] )
    return templates

CHSNUM_LIST = {
    0:  "零" ,
    1:  "一" ,
    2:  "二" ,
    3:  "三" ,
    4:  "四" ,
    5:  "五" ,
    6:  "六" ,
    7:  "七" ,
    8:  "八" ,
    9:  "九" ,
    10: "十" ,
    11: "十一" ,
    12: "十二"
}

def conv_date_to_chs( date: str ) -> str:
    date_obj = datetime.strptime( date , "%Y-%m-%d" )
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    chs_date = ""
    
    while year > 0:
        chs_date = CHSNUM_LIST[year%10] + chs_date
        year //= 10
    chs_date += "年"

    chs_date += CHSNUM_LIST[month] + "月"

    if day <= 12:
        chs_date += CHSNUM_LIST[day]
    else:
        if day >= 20:
            chs_date += CHSNUM_LIST[day//10]
        chs_date += "十"
        if day % 10 != 0:
            chs_date += CHSNUM_LIST[day%10]
    chs_date += "日"        

    return chs_date

def create_article() -> None:
    with open( "./template/article.html.in" , 'r' , encoding = "utf-8" ) as rFile:
        template_text = rFile.read()
    filename = input( "HTML Filename: " )
    title = input( "Article Title: " )
    first_wrote_time = input( "First Wrote Time (YYYY-MM-DD): " )
    wrote_time = input( "Wrote Time (YYYY-MM-DD): " )

    in_head_title = title + " Ace_Radom's Blog"
    in_title = title
    in_first_wrote_time = first_wrote_time
    in_wrote_time = conv_date_to_chs( wrote_time )
    template_text = template_text.replace( "%HEAD_TITLE%" , in_head_title )
    template_text = template_text.replace( "%TITLE%" , in_title )
    template_text = template_text.replace( "%FIRST_WROTE_TIME%" , in_first_wrote_time )
    template_text = template_text.replace( "%WROTE_TIME%" , in_wrote_time )

    with open( f"../text/{ filename }.html" , 'w' , encoding = "utf-8" ) as wFile:
        wFile.write( template_text )

TEMPLATE_PARSER = {
    "article": create_article
}

def main():
    print( "Available templates:" )
    templates = get_templates()
    counter = 1
    for template in templates:
        print( f"  { counter }. { template }" )
        counter += 1
    template_choose_input = input( "Please choose the template to use: " )
    try:
        template_choose_num = int( template_choose_input )
        if template_choose_num >= counter:
            raise ValueError
    except ValueError:
        print( "Illegal input, exit" )
        exit( 1 )

    TEMPLATE_PARSER[templates[template_choose_num-1]]()

if __name__ == "__main__":
    main()
