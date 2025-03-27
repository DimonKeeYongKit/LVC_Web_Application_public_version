# import the class
from crawler import *
from preprocessing_data import *
from connectToDatabase import *

# import flask framework
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

# window dialog library
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

# import other used library
from os import listdir

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/display')
def display():
    platform = session.get('platform')
    dataset = session.get('current_dataset')
    heading = ['Error platform']
    if platform == 'Facebook' or platform == 'Twitter':
        heading = ['No', 'post_id', 'post_content', 'post_date', 'post_time', 'post_url', 'author_id', 'author_name',
                   'crawl_date', 'crawl_time']
    elif platform == 'Reddit':
        heading = ['No', 'post_id', 'post_title', 'post_content', 'post_date', 'post_time', 'post_url', 'author_id',
                   'author_name', 'crawl_date', 'crawl_time']

    return render_template('display.html', data=dataset, length=len(dataset), platform=platform, heading=heading)


@app.route('/display_lite')
def display_lite():
    platform = session.get('platform')
    dataset = session.get('lite_dataset')
    heading = ['No', 'post_id', 'post_content', 'post_date', 'post_time']
    return render_template('display_lite.html', data=dataset, length=len(dataset), platform=platform, heading=heading)


@app.route('/web_crawler', methods=["POST", "GET"])
def crawler():
    if request.method == "POST":
        try:
            selection = request.form['platform_selection']
        except:
            error_msg = 'Please select one platform'
            return render_template('web_crawler.html', error_msg=error_msg)

        choice = request.form['submit_btn']
        if choice == 'new':
            if selection == 'Facebook':
                return redirect(url_for("fb_crawler"))
            elif selection == 'Reddit':
                return redirect(url_for("rd_crawler"))
            elif selection == 'Twitter':
                return redirect(url_for("tt_crawler"))
        elif choice == 'exist':
            return redirect(url_for('exist_crawler', platform=selection))

    else:
        return render_template('web_crawler.html')


@app.route('/Facebook_crawler', methods=["POST", "GET"])
def fb_crawler():
    if request.method == "POST":
        page_id = request.form['page_id']
        quantity = request.form['quantity']

        # check save database radio button
        try:
            save_choice = request.form['save_check']
        except:
            save_choice = False

        dataset, exist_count = crawl_Facebook_post(page_id, int(quantity))
        if not dataset:
            error_msg = 'Invalid page_id. Please input the valid page_id.'
            return render_template('Facebook_crawler.html', error_msg=error_msg)

        session['platform'] = 'Facebook'

        if dataset:
            if save_choice:
                save_crawler_workbook(page_id, "Post", "Facebook", dataset)

            lite_dataset = []
            for row in dataset:
                current = []
                for data in row[0:4]:
                    current.append(data)
                lite_dataset.append(current)

            session['current_dataset'] = dataset
            session['lite_dataset'] = lite_dataset

            return redirect(url_for('display_lite'))
        else:
            return render_template('empty.html')
    else:
        return render_template('Facebook_crawler.html')


@app.route('/Reddit_crawler', methods=["POST", "GET"])
def rd_crawler():
    if request.method == "POST":
        topic = request.form['topic']
        quantity = request.form['quantity']
        try:
            save_choice = request.form['save_check']
        except:
            save_choice = False

        dataset, exist_count = crawl_Reddit_post(topic, int(quantity))
        if not dataset:
            error_msg = 'Invalid page_id. Please input the valid page_id.'
            return render_template('Reddit_crawler.html', error_msg=error_msg)

        session['platform'] = 'Reddit'

        if dataset:
            if save_choice:
                save_crawler_workbook(topic, "Post", "Reddit", dataset)

            lite_dataset = []
            for row in dataset:
                current = []
                for data in row[0:2]:
                    current.append(data)
                for data in row[3:5]:
                    current.append(data)
                lite_dataset.append(current)
            session['current_dataset'] = dataset
            session['lite_dataset'] = lite_dataset

            return redirect(url_for('display_lite'))
        else:
            return render_template('empty.html')
    else:
        return render_template('Reddit_crawler.html')


@app.route('/Twitter_crawler', methods=["POST", "GET"])
def tt_crawler():
    if request.method == "POST":
        keyword = request.form['keyword']
        quantity = request.form['quantity']
        try:
            save_choice = request.form['save_check']
        except:
            save_choice = False

        dataset, exist_count = crawl_Twitter_post(keyword, int(quantity))

        if not dataset:
            error_msg = 'Invalid page_id. Please input the valid page_id.'
            return render_template('Twitter_crawler.html', error_msg=error_msg)

        session['platform'] = 'Twitter'

        if dataset:
            if save_choice:
                save_crawler_workbook(keyword, "Post", "Twitter", dataset)

            lite_dataset = []
            for row in dataset:
                current = []
                for data in row[0:4]:
                    current.append(data)
                lite_dataset.append(current)

            session['current_dataset'] = dataset
            session['lite_dataset'] = lite_dataset

            return redirect(url_for('display_lite'))
        else:
            return render_template('empty.html')
    else:
        return render_template('Twitter_crawler.html')


@app.route('/exist_crawler/<platform>', methods=["POST", "GET"])
def exist_crawler(platform):
    if platform != 'Facebook' and platform != 'Reddit' and platform != 'Twitter':
        return render_template('invalid_platform.html')

    id_list = listdir("./Database/" + platform + "/Post/")
    if id_list:
        book_name = []
        for id in id_list:
            book_name.append(id.replace('.xlsx', ''))
    else:
        return render_template('empty.html')
    if request.method == "POST":

        dataset = []
        selection = request.form.getlist('exist_list')
        if not selection:
            error_msg = "At least one ID Required..."
            return render_template('exist_selection.html',
                                   data=book_name, length=len(book_name), platform=platform, error_msg=error_msg)

        quantity = request.form['quantity']
        try:
            save_choice = request.form['save_check']
        except:
            save_choice = False

        if not quantity:
            quantity = 10

        for select in selection:
            ds, ex_count = crawl_post(select, int(quantity), platform)
            if save_choice:
                save_crawler_workbook(select, "Post", platform, ds)
            dataset = dataset + ds

        if not dataset:
            return render_template('empty.html')

        lite_dataset = []
        if platform == 'Facebook' or platform == 'Twitter':
            for row in dataset:
                current = []
                for data in row[0:4]:
                    current.append(data)
                lite_dataset.append(current)
        elif platform == 'Reddit':
            for row in dataset:
                current = []
                for data in row[0:2]:
                    current.append(data)
                for data in row[3:5]:
                    current.append(data)
                lite_dataset.append(current)

        session['platform'] = platform
        session['current_dataset'] = dataset
        session['lite_dataset'] = lite_dataset

        return redirect(url_for('display_lite'))

    else:
        return render_template('exist_selection.html', data=book_name, length=len(book_name), platform=platform)


@app.route('/preprocessing_platform_selection', methods=["POST", "GET"])
def preprocessing_platform_selection():
    if request.method == "POST":
        try:
            selection = request.form['platform_selection']
        except:
            error_msg = 'Please select one platform'
            return render_template('preprocessing_platform_selection.html', error_msg=error_msg)

        return redirect(url_for("preprocessing_selection", platform=selection))
    else:
        return render_template('preprocessing_platform_selection.html')


@app.route('/preprocessing_selection/<platform>', methods=["POST", "GET"])
def preprocessing_selection(platform):
    id_list = listdir("./Database/" + platform + "/Post/")
    if not id_list:
        return render_template('empty.html')
    book_name = []
    for id in id_list:
        book_name.append(id.replace('.xlsx', ''))
    if request.method == "POST":
        dataset = []
        selection = request.form.getlist('exist_list')
        if not selection:
            error_msg = "At least one ID Required..."
            return render_template('preprocessing_selection.html',
                                   data=book_name, length=len(book_name), platform=platform, error_msg=error_msg)

        print(selection)

        for select in selection:
            ds = load_crawler_workbook(select.replace('.xlsx', ''), "Post", platform)
            dataset = dataset + ds

        if dataset:
            session['current_dataset'] = dataset
            session['platform'] = platform
            return redirect(url_for('preprocessing_preview'))
        else:
            return render_template('empty.html')
    else:
        return render_template('preprocessing_selection.html', data=book_name, length=len(book_name),
                               platform=platform)


@app.route('/preprocessing_preview', methods=["POST", "GET"])
def preprocessing_preview():
    if request.method == "POST":
        print("POST")
    else:
        dataset = session.get('current_dataset')
        return render_template('preprocessing_preview.html',
                               heading=['No', 'Post'], data=dataset, length=len(dataset), platform=session['platform'])


@app.route('/preprocessing_result', methods=["POST", "GET"])
def preprocessing_result():
    dataset = session.get('current_dataset')
    length = len(dataset)
    selected = []
    out1 = []
    out2 = []
    for data in dataset:
        d1, d2 = full_preprocessing(data)
        out1.append(d1)
        out2.append(d2)
    if request.method == "POST":

        choice = request.form['type']
        if choice == 'org':
            for data in dataset:
                current = [str(data)]
                selected.append(current)
        elif choice == 'pre':
            for data in out1:
                current = [str(data)]
                selected.append(current)
        elif choice == 'tag':
            for data in out2:
                current = [str(data)]
                selected.append(current)

        try:
            root = Tk()
            root.withdraw()
            # ensure the file dialog pops to the top window
            root.wm_attributes('-topmost', 1)
            name = datetime.date.today().strftime('%d-%m-%Y') + " " + datetime.datetime.now().time().strftime(
                '%H_%M_%S')
            filetypes = [("Excel files", "*.xlsx"), ]
            file = asksaveasfilename(initialdir=".//Database//Processed", title='Save the workbook', initialfile=name,
                                     filetypes=filetypes, parent=root)

            # reload when close the dialog
            if not file:
                return render_template('preprocessing_result.html', length=length, org_data=dataset, choice1=out1,
                                       choice2=out2, platform=session['platform'])
            file += '.xlsx'

            wb = Workbook()
            wbs = wb.active
            for select in selected:
                wbs.append(select)
            wb.save(file)
            wb.close()
        except:
            return render_template('error_save_file.html')
        return render_template('save_file_done.html', file_path=file)
    else:
        return render_template('preprocessing_result.html', length=length, org_data=dataset, choice1=out1,
                               choice2=out2, platform=session['platform'])


@app.route('/list_of_tag')
def list_of_tag():
    return render_template('list_of_tag.html')


@app.route('/developing')
def developing():
    return render_template('developing.html')


@app.route('/empty')
def empty():
    return render_template('empty.html')


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html"), 404


# Invalid Server Error
@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    return render_template("500.html"), 500


# handle all error
@app.errorhandler(Exception)
def all_exception_handler(e):
    print(e)
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)
