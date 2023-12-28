
from flask.views import View, MethodView
from . import api
from flask import jsonify, request
from app.models import Course, db, course_schema, courses_schema


#Vista RUTA blueprint
@api.route('/api')
def api2():
    return('Hola API')


#Vista basada en una clase
class ShowApi(View):
    def dispatch_request(self):
        return "Vista de clase"
    
api.add_url_rule('/clase', view_func=ShowApi.as_view('show_api'))


class ApiCourse(MethodView):
    def get(self, course_id = None):
        
        if isinstance(course_id, str):
            courses = Course.query.filter_by(coursename=course_id).first()
            course_json = course_schema.dump(courses)
            return jsonify(course_json)
        
        elif isinstance(course_id, int):
            courses = Course.query.get_or_404(course_id)
            course_json = course_schema.dump(courses)
            return jsonify(course_json)
        
        else:
            courses = Course.query.all()
            courses_json = courses_schema.dump(courses)
            return jsonify(courses_json)
        

    def post(self):
        coursename = request.json['coursename']
        hours = request.json['hours']
        tutor_id = request.json['tutor_id']

        
        my_course = Course(coursename, hours, tutor_id)
        db.session.add(my_course)
        db.session.commit()

        return course_schema.jsonify(my_course)
    
    
    def put(self, course_id):
        course = Course.query.get(course_id)
        
        coursename = request.json['coursename']
        hours = request.json['hours']
        tutor_id = request.json['tutor_id']
        
        course.coursename = coursename
        course.hours = hours
        course.tutor_id = tutor_id

        db.session.commit()
        return course_schema.jsonify(course)
    
    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return course_schema.jsonify(course)


api.add_url_rule('/apicursos', methods=['GET', 'POST'], view_func=ApiCourse.as_view('api_cursos'))
api.add_url_rule('/apicursos/<int:course_id>', methods=['GET', 'POST', 'PUT', 'DELETE'], view_func=ApiCourse.as_view('api_cursos_id'))
api.add_url_rule('/apicursos/<string:course_id>', methods=['GET', 'POST', 'PUT', 'DELETE'], view_func=ApiCourse.as_view('api_cursos_name'))