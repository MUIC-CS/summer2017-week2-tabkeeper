from person import PeopleRepo
from borrowal import BorrowalRepo
from flask import Flask, render_template, request, url_for, redirect, abort

app = Flask('TabKeeper')


@app.route('/')
def index():
    people = PeopleRepo.find_all()
    return render_template('index.html', people=people)


@app.route('/profile/<name>')
def profile(name):
    lender = PeopleRepo.find_by_name(name)
    if lender is None:
        abort_400("name %s not found" % name)
    others = [x for x in PeopleRepo.find_all() if x.id != lender.id]

    def summarize(other):
        return {
            'other': other,
            'total': BorrowalRepo.summarize_debt(lender, other)
        }
    summaries = [
        summarize(other) for other in others if other.id != lender.id
    ]

    return render_template(
        'profile.html',
        others=others,
        lender=lender,
        summaries=summaries
    )


@app.route('/history/<left>/<right>')
def history(left, right):
    left_name, right_name = left, right
    left = PeopleRepo.find_by_name(left)
    right = PeopleRepo.find_by_name(right)
    if left is None or right is None:
        abort_400('person not found %s, %s' % (left_name, right_name))
    print left.id, right.id
    lends = BorrowalRepo.find_by_lender_borrower(left, right)
    borrows = BorrowalRepo.find_by_lender_borrower(right, left)
    total = BorrowalRepo.summarize_debt(left, right)
    return render_template('history.html',
                           left=left,
                           right=right,
                           lends=lends,
                           borrows=borrows,
                           total=total)


@app.route('/lend', methods=['POST'])
def lend():
    print request.form
    lender_name = request.form['lender']
    lender = PeopleRepo.find_by_name(lender_name)
    if lender is None:
        abort_400('person not found %s' % (lender_name))

    amount = float(request.form['amount'])
    description = request.form['description']
    borrower_name = request.form['to']
    borrower = PeopleRepo.find_by_name(borrower_name)

    BorrowalRepo.create_transaction(lender, borrower, amount, description)
    return redirect(url_for('profile', name=lender.name))


def abort_400(msg):
    print 'Abort 400: %s' % msg
    abort(400)


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
