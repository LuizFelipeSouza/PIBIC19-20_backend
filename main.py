from flask import Flask
from requests import RequestException
import os
from sumarizador import main
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class SumarizadorError(Exception):
    def __init__(self, mensagem, status_code=None, payload=None):
        Exception.__init__(self)
        self.mensagem = mensagem
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.mensagem
        return rv


class ConexaoError(Exception):
    def __init__(self, mensagem, status_code=None, payload=None):
        Exception.__init__(self)
        self.mensagem = mensagem
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.mensagem
        return rv


@app.route('/<titulo_do_artigo>')
def sumarizar(titulo_do_artigo):
    try:
        arquivo_json = main(titulo_do_artigo)
    except ZeroDivisionError:
        mensagem = "Houve um erro na sumarização. Por favor, contate os desenvolvedores"
        # 500 é o código para internal server error
        raise SumarizadorError(mensagem, status_code=500)
    except KeyError:
        mensagem = "Página não encontrada. Verifique se há erros de digitação!"
        # 404 é o código para página não encontrada
        raise ConexaoError(mensagem, status_code=404)
    except RequestException:
        mensagem = "Erro ao se comunicar com a Wikipédia. Verifique sua conexão!"
        # 503 é o código para service unavailable
        raise ConexaoError(mensagem, status_code=503)
    else:
        # retorna um JSON com os títulos dos tópicos e seus respectivos conteúdos sumarizados
        return arquivo_json


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
