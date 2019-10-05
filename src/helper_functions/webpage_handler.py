'''
Creates and open webpage containing retrieved images
'''
import os

import webbrowser

WEBPAGE_FILENAME = "mars_rover_images.html"


def add_header(file):
    '''Add head and header in the html file'''
    file.write("<!doctype html>\n")
    file.write("<html lang='en'>\n")
    file.write("  <head>\n")
    file.write("    <!-- Required meta tags -->\n")
    file.write("    <meta charset='utf-8'>\n")
    file.write("    <meta name='viewport' content='width=device-width, \
                initial-scale=1, shrink-to-fit=no'>\n")

    file.write("    <!-- Bootstrap CSS -->\n")
    file.write("    <link rel='stylesheet' href='bootstrap/bootstrap.min.css' \
                integrity='sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T' \
                crossorigin='anonymous'>\n")

    file.write("    <title>Mars Rover Images</title>\n")
    file.write("  </head>\n")
    file.write("  <body>\n")
    file.write("     <div class='container'>\n")
    file.write("        <nav class='navbar navbar=expand-lg navbar-light bg-light'>")
    file.write("           Mars Rover Images")
    file.write("        </nav>")
    file.write("      </div>")

def add_js_files(file):
    '''Add javascript files in the body in the html file'''
    file.write("    <script src='bootstrap/jquery-3.3.1.slim.min.js' \
                integrity='sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo' \
                crossorigin='anonymous'></script>\n")
    file.write("    <script src='bootstrap/popper.min.js\
                integrity='sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1' \
                crossorigin='anonymous'></script>\n")
    file.write("    <script src='bootstrap/bootstrap.min.js' \
                integrity='sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM' \
                crossorigin='anonymous'></script>\n")
    file.write("  </body>\n")

def add_carousel_control(file):
    '''Add prev and next for carousel'''
    file.write("              <a class='carousel-control-prev' href='#carouselImages' \
                role='button' data-slide='prev'>\n")
    file.write("                <span class='carousel-control-prev-icon' \
                aria-hidden='true'></span>\n")
    file.write("                <span class='sr-only'>Previous</span>\n")
    file.write("              </a>\n")
    file.write("              <a class='carousel-control-next' href='#carouselImages' \
                role='button' data-slide='next'>\n")
    file.write("                <span class='carousel-control-next-icon' \
                aria-hidden='true'></span>\n")
    file.write("                <span class='sr-only'>Next</span>\n")
    file.write("              </a>\n")

def add_images_to_carousel(file, date_directory):
    '''Add image files to carousel'''
    one_active = False
    for _, _, img_files in os.walk(date_directory):
        for img_file in img_files:
            if img_file.endswith(".jpg") or img_file.endswith(".JPG"):
                if one_active is False:
                    file.write("                <div class='carousel-item active'>\n")
                    one_active = True
                else:
                    file.write("                <div class='carousel-item'>\n")

                string = "                <img src='" \
                        + os.path.join(date_directory, img_file) \
                        + "' class='d-block w-100' alt='...'>\n"
                file.write(string)
                file.write("                </div>\n")

def create_webpage(download_location, dates):
    '''Function for creating webpage'''
    with open(WEBPAGE_FILENAME, "w") as file:
        add_header(file)
        file.write("<div class='container'>\n")
        file.write("    <div class='accordion' id='imageAccordion'>\n")
        one_card_active = False
        for one_date in dates:
            aria_expanded = ""
            class_collapse = ""
            if one_card_active is False:
                one_card_active = True
                aria_expanded = "true"
                class_collapse = "collapse show"
            else:
                aria_expanded = "false"
                class_collapse = "collapse"

            date_card_id = "card" + one_date
            date_collapse_id = "collapse" + one_date

            file.write("      <div class='card'>\n")
            string = "      <div class='card-header' id='" + date_card_id + "'>\n"
            file.write(string)

            file.write("          <h2 class='mb-0'>\n")

            string = "          <button class='btn btn-link' type='button' \
                    data-toggle='collapse' data-target='#" + date_collapse_id \
                    + "' aria-expanded='" + aria_expanded + "' aria-controls='" \
                    + date_collapse_id + "'>\n"
            file.write(string)

            file.write(one_date)
            file.write("            </button>\n")
            file.write("          </h2>\n")
            file.write("        </div>\n")

            string = "      <div id='" + date_collapse_id + "' class='" + class_collapse \
                    + "' aria-labelledby='" + date_card_id \
                    + "' data-parent='#imageAccordion'>\n"
            file.write(string)

            file.write("          <div class='card-body'>\n")
            file.write("            <div id='carouselImages' class='carousel slide' \
                        data-ride='carousel'>\n")
            file.write("              <div class='carousel-inner'>\n")

            #Get images in date directory
            date_directory = os.path.join(download_location, one_date)
            add_images_to_carousel(file, date_directory)

            file.write("              </div>\n")
            add_carousel_control(file)
            file.write("            </div>\n")
            file.write("          </div>\n")
            file.write("        </div>\n")
            file.write("      </div>\n")

        file.write("    </div>\n")
        file.write("</div>\n")
        add_js_files(file)

def open_webpage():
    '''Function for opening webpage in browser'''
    webbrowser.open('file://' + os.path.realpath(WEBPAGE_FILENAME))
