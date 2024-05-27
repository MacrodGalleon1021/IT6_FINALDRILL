from flask import Flask, make_response, jsonify, request
import pymysql

app = Flask(__name__)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "macrod"
app.config["MYSQL_DB"] = "sampledb"

def get_connection():
    return pymysql.connect(
        host="localhost",
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        db=app.config["MYSQL_DB"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
@app.route("/")
def hello_world():
    return "<p> HELLO WORLD!</p>"

@app.route("/branches", methods=["GET"])
def get_branches():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM branches"
            cursor.execute(query)
            data = cursor.fetchall()

        return make_response(jsonify(data), 200)
    finally:
        connection.close()
@app.route("/branches/<int:branch_id>", methods=["GET"])
def get_branch_by_id(branch_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM branches WHERE branch_id = %s"
            cursor.execute(query, (branch_id,))
            data = cursor.fetchone()

        if data:
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({"error": "branch not found"}), 404)
    finally:
        connection.close()

@app.route("/branches", methods=["POST"])
def add_branch():
    connection = get_connection()
    cur = connection.cursor()
    info = request.get_json()
    branch_name = info["branch_name"]
    location = info["location"]
    cur.execute(
        """ INSERT INTO branches (branch_name, location) VALUE (%s, %s)""",
        (branch_name, location),
    )
    connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "branch added successfully", "rows_affected": rows_affected}
        ),
        201,
    )
   

@app.route("/branches/<int:id>", methods=["PUT"])
def update_branch(id):
    connection = get_connection()
    cur = connection.cursor()
    info = request.get_json()
    branch_name = info["branch_name"]
    location = info["location"]
    cur.execute(
        """ UPDATE branches SET branch_name = %s, location= %s WHERE branch_id = %s """,
        (branch_name, location, id),
    )
    connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "branch updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/branches/<int:id>", methods=["DELETE"])
def delete_branch(id):
    connection = get_connection()
    cur = connection.cursor()
    cur.execute(""" DELETE FROM branches where branch_id = %s """, (id,))
    connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "branch deleted successfully", "rows_affected": rows_affected}),
        200,
    )

@app.route("/branches/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo =request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)