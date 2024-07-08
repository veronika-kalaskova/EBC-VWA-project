from flask import Blueprint, render_template, request, flash

import auth
import forms
from service.category_service import CategoryService
from service.product_service import ProductService

products = Blueprint('products', __name__)


@products.route('/')
def list():
    price_limit = request.args.get('price_limit', None, int)
    category_id = request.args.get('category_id', None, int)
    search = request.args.get('search', None, str)

    products = ProductService.get_all(price_limit, category_id, search)
    category = CategoryService.get_by_id(category_id) if category_id is not None else None

    return render_template(
        "products/list.jinja",
        price_limit=price_limit,
        products=products,
        category_id=category_id,
        category=category,
        search=search
    )


@products.route('/new', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required('admin', 'salesman')
def new():
    form = forms.AddProductForm(request.form)
    categories = CategoryService.get_all()
    form.category_id.choices = [(item['id'], item['name']) for item in categories]

    if request.method == 'POST' and form.validate():
        ProductService.insert_product(
            name=request.form['name'],
            price=request.form['price'],
            img=request.form['img'],
            category_id=request.form['category_id'],
        )
        flash('Product inserted')
    return render_template('products/new.jinja', form=form)


@products.route('/<id>/delete')
def delete(id):
    # Future TODO
    return "TODO delete product with ID=" + id
