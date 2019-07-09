from bottle import Bottle, request, response, route
import subprocess, random, io

app = Bottle()

@app.error(404)
def error404(error):
    return "This is samsa. Try /swagger"

@app.route('/v2tov3', method='POST')
def convert_v2_to_v3():

    try:
        syntax = request.query['format']
    except:
        syntax = "json"

    r = str(random.randint(1000,9999))
    f = "/tmp/" + r + ".api"
    with io.open(f, 'w', encoding="utf-8") as outfile:
        outfile.write(unicode(request.body.read()))
    outfile.close()

    converted = "/tmp/" + r + ".api_out"
    output = subprocess.check_output(['api-spec-converter', '-s', syntax, '--from=swagger_2', '--to=openapi_3', f])

    if syntax == "json":
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    else:
        response.headers['Content-Type'] = 'text/yaml; charset=UTF-8'

    return output

@app.route('/v3tov2', method='POST')
def convert_v3_to_v2():

    try:
        syntax = request.query['format']
    except:
        syntax = "json"

    r = str(random.randint(1000,9999))
    f = "/tmp/" + r + ".api"
    with io.open(f, 'w', encoding="utf-8") as outfile:
        outfile.write(unicode(request.body.read()))
    outfile.close()

    converted = "/tmp/" + r + ".api_out"
    output = subprocess.check_output(['api-spec-converter', '-s', syntax, '--from=openapi_3', '--to=swagger_2', f])

    if syntax == "json":
        response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    else:
        response.headers['Content-Type'] = 'text/yaml; charset=UTF-8'

    return output

@app.get('/swagger')
def swagger():

    swagger = '''{
        "swagger": "2.0",
        "info": {
            "version": "",
            "title": "samsa",
            "description": "Convert between OpenAPI v2 and v3 formats (YAML/JSON)"
        },
        "basePath": "/convert",
        "paths": {
            "/v3tov2": {
                "get": {
                    "operationId": "GET_v3tov2",
                    "summary": "OpenAPI 3.0 to Swagger",
                    "parameters": [
                        {
                            "name": "format",
                            "in": "query",
                            "type": "string",
                            "enum": [
                                "json",
                                "yaml"
                            ]
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": ""
                        },
                        "400": {
                            "description": ""
                        }
                    }
                }
            },
            "/v2tov3": {
                "get": {
                    "operationId": "v2tov3",
                    "summary": "Swagger to OpenAPI 3.0",
                    "parameters": [
                        {
                            "name": "format",
                            "in": "query",
                            "type": "string",
                            "enum": [
                                "json",
                                "yaml"
                            ]
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": ""
                        },
                        "400": {
                            "description": ""
                        }
                    }
                }
            }
        },
        "definitions": {}
    }'''

    response.headers['Content-Type'] = 'application/json; charset=UTF-8'
    return swagger