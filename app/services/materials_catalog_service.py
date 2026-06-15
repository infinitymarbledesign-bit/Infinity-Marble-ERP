"""Materials catalog service"""
from database import db
from database.models import Material

class MaterialsCatalogService:
    """Service for managing materials catalog"""
    
    @staticmethod
    def seed_marble_materials():
        """
        Seed database with premium marble materials
        """
        marble_materials = [
            {
                'name': 'Italian Carrara Marble',
                'material_type': 'marble',
                'code': 'MAR-CARRARA-001',
                'description': 'Premium white Carrara marble from Italy with fine grain',
                'color': 'White',
                'finish': 'Polished',
                'price_per_sqft': 25.00,
                'price_per_meter': 268.90,
                'density': 2700,
                'mohs_hardness': 3.0,
                'origin': 'Carrara, Italy',
                'supplier': 'Italian Marble Imports Ltd',
                'stock_quantity': 500,
                'reorder_level': 100
            },
            {
                'name': 'Black Galaxy Granite',
                'material_type': 'marble',
                'code': 'MAR-GALAXY-001',
                'description': 'Elegant black granite with golden flecks from India',
                'color': 'Black with Gold Flecks',
                'finish': 'Polished',
                'price_per_sqft': 18.00,
                'price_per_meter': 193.75,
                'density': 2750,
                'mohs_hardness': 7.0,
                'origin': 'Bangalore, India',
                'supplier': 'Galaxy Granite Works',
                'stock_quantity': 750,
                'reorder_level': 150
            },
            {
                'name': 'Statuario Marble',
                'material_type': 'marble',
                'code': 'MAR-STATUARIO-001',
                'description': 'Classic white Statuario with bold gray veining',
                'color': 'White with Gray Veins',
                'finish': 'Polished',
                'price_per_sqft': 28.00,
                'price_per_meter': 301.38,
                'density': 2700,
                'mohs_hardness': 3.0,
                'origin': 'Tuscany, Italy',
                'supplier': 'Italian Marble Imports Ltd',
                'stock_quantity': 400,
                'reorder_level': 80
            },
            {
                'name': 'Rosso Levanto Marble',
                'material_type': 'marble',
                'code': 'MAR-ROSSO-001',
                'description': 'Rich red marble with white and black veining',
                'color': 'Red',
                'finish': 'Polished',
                'price_per_sqft': 22.00,
                'price_per_meter': 236.80,
                'density': 2750,
                'mohs_hardness': 3.5,
                'origin': 'Levanto, Italy',
                'supplier': 'Italian Marble Imports Ltd',
                'stock_quantity': 300,
                'reorder_level': 60
            },
            {
                'name': 'Emperador Dark Marble',
                'material_type': 'marble',
                'code': 'MAR-EMPERADOR-001',
                'description': 'Deep brown Emperador marble with golden tones',
                'color': 'Dark Brown',
                'finish': 'Polished',
                'price_per_sqft': 20.00,
                'price_per_meter': 215.27,
                'density': 2710,
                'mohs_hardness': 3.0,
                'origin': 'Spain',
                'supplier': 'Spanish Marble Corp',
                'stock_quantity': 600,
                'reorder_level': 120
            },
            {
                'name': 'Calacatta Marble',
                'material_type': 'marble',
                'code': 'MAR-CALACATTA-001',
                'description': 'Premium white Calacatta with bold gold and gray veining',
                'color': 'White with Gold Veins',
                'finish': 'Polished',
                'price_per_sqft': 32.00,
                'price_per_meter': 344.44,
                'density': 2700,
                'mohs_hardness': 3.0,
                'origin': 'Tuscany, Italy',
                'supplier': 'Italian Marble Imports Ltd',
                'stock_quantity': 350,
                'reorder_level': 70
            },
            {
                'name': 'Portoro Black Marble',
                'material_type': 'marble',
                'code': 'MAR-PORTORO-001',
                'description': 'Luxurious black marble with gold veining',
                'color': 'Black with Gold Veins',
                'finish': 'Polished',
                'price_per_sqft': 30.00,
                'price_per_meter': 322.92,
                'density': 2730,
                'mohs_hardness': 3.0,
                'origin': 'Tuscany, Italy',
                'supplier': 'Italian Marble Imports Ltd',
                'stock_quantity': 250,
                'reorder_level': 50
            },
            {
                'name': 'Vermont Danby Marble',
                'material_type': 'marble',
                'code': 'MAR-DANBY-001',
                'description': 'Pure white marble from American quarries',
                'color': 'Pure White',
                'finish': 'Polished',
                'price_per_sqft': 26.00,
                'price_per_meter': 279.87,
                'density': 2700,
                'mohs_hardness': 3.0,
                'origin': 'Vermont, USA',
                'supplier': 'American Marble Works',
                'stock_quantity': 400,
                'reorder_level': 80
            },
        ]
        
        for material in marble_materials:
            existing = Material.query.filter_by(code=material['code']).first()
            if not existing:
                m = Material(**material)
                db.session.add(m)
        
        db.session.commit()
        return len(marble_materials)
    
    @staticmethod
    def seed_porcelain_materials():
        """
        Seed database with premium porcelain tiles
        """
        porcelain_materials = [
            {
                'name': 'Marble Effect Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-MARBLE-001',
                'description': 'High-quality porcelain tile with marble effect finish',
                'color': 'White with Gray Veins',
                'finish': 'Polished',
                'price_per_sqft': 12.00,
                'price_per_meter': 129.17,
                'density': 2400,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 2000,
                'reorder_level': 400
            },
            {
                'name': 'Slate Effect Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-SLATE-001',
                'description': 'Rustic slate effect porcelain tiles',
                'color': 'Gray',
                'finish': 'Textured',
                'price_per_sqft': 10.00,
                'price_per_meter': 107.64,
                'density': 2350,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 2500,
                'reorder_level': 500
            },
            {
                'name': 'Wood Effect Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-WOOD-001',
                'description': 'Realistic wood-look porcelain tiles',
                'color': 'Walnut Brown',
                'finish': 'Matte',
                'price_per_sqft': 11.50,
                'price_per_meter': 123.75,
                'density': 2380,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 1500,
                'reorder_level': 300
            },
            {
                'name': 'Granite Effect Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-GRANITE-001',
                'description': 'Durable granite effect porcelain tiles',
                'color': 'Black with Speckles',
                'finish': 'Polished',
                'price_per_sqft': 10.50,
                'price_per_meter': 113.02,
                'density': 2400,
                'mohs_hardness': 8.5,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 2000,
                'reorder_level': 400
            },
            {
                'name': 'Cement Look Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-CEMENT-001',
                'description': 'Industrial cement look porcelain tiles',
                'color': 'Light Gray',
                'finish': 'Matte',
                'price_per_sqft': 9.50,
                'price_per_meter': 102.26,
                'density': 2350,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 3000,
                'reorder_level': 600
            },
            {
                'name': 'Terrazzo Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-TERRAZZO-001',
                'description': 'Contemporary terrazzo effect porcelain tiles',
                'color': 'Multi-colored',
                'finish': 'Polished',
                'price_per_sqft': 13.00,
                'price_per_meter': 139.93,
                'density': 2400,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 1200,
                'reorder_level': 240
            },
            {
                'name': 'Concrete Effect Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-CONCRETE-001',
                'description': 'Raw concrete effect porcelain tiles',
                'color': 'Dark Gray',
                'finish': 'Matte',
                'price_per_sqft': 10.00,
                'price_per_meter': 107.64,
                'density': 2380,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 2200,
                'reorder_level': 440
            },
            {
                'name': 'Limestone Effect Porcelain Tile',
                'material_type': 'porcelain',
                'code': 'POR-LIMESTONE-001',
                'description': 'Elegant limestone effect porcelain tiles',
                'color': 'Cream',
                'finish': 'Textured',
                'price_per_sqft': 11.00,
                'price_per_meter': 118.38,
                'density': 2350,
                'mohs_hardness': 8.0,
                'origin': 'China',
                'supplier': 'Premium Ceramics Ltd',
                'stock_quantity': 1800,
                'reorder_level': 360
            },
        ]
        
        for material in porcelain_materials:
            existing = Material.query.filter_by(code=material['code']).first()
            if not existing:
                m = Material(**material)
                db.session.add(m)
        
        db.session.commit()
        return len(porcelain_materials)
