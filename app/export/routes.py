from flask import render_template

from app.export import export_bp

def init_app(app):
    """Inicializa o módulo de exportação na aplicação Flask"""
    app.register_blueprint(export_bp)
    
    # Rota para a página principal de exportação
    @export_bp.route('/', methods=['GET'])
    def export_index():
        """Renderiza a página principal de exportação"""
        return render_template('export/export.html')
