from handlers.base import BaseHandler, TemplateRendering


class SwaggerHandler(BaseHandler, TemplateRendering):
    def get(self):
        self.write(self.render_template("index.html"))
