from ..forms.plant_type import PlantTypeForm
from ..models.plant_type import PlantTypeModel, db
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import OperationalError


plant_type_bp = Blueprint('plant_type', __name__, url_prefix='/plant_type')


@plant_type_bp.context_processor
def utility_title(title='Plant Type'):
    return dict(title=title)


@plant_type_bp.context_processor
def utility_human_readable_time():
    def human_readable_time(quotient):
        """quotient input is the time in seconds"""
        if quotient is None or quotient < 0:
            return None
        reminder = unit = unit_prev = 0
        dividers = [(60, 's', None), (60, 'm', 's'), (24, 'h', 'm'), (7, 'd', 'h'), (52, 'w', 'd'), (-1, 'y', 'w')]
        for divider, unit, unit_prev in dividers:
            if divider < 0 or quotient < divider:
                break
            quotient, reminder = divmod(quotient, divider)
        return f'{quotient}{unit}' + \
               (f'{reminder}{unit_prev}' if reminder > 0 else '')
    return dict(human_readable_time=human_readable_time)


@plant_type_bp.route('/')
def list_all():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=15, type=int)
    try:
        plant_types = PlantTypeModel.query.order_by(PlantTypeModel.name.asc())\
            .paginate(page, size)
    except OperationalError:
        plant_types = None

    return render_template('plant_type/list.html',
                           plant_types=plant_types,
                           size=size)


@plant_type_bp.route('/<int:plant_type_id>')
def details(plant_type_id):
    plant_type = PlantTypeModel.query.get_or_404(plant_type_id)
    return render_template('plant_type/details.html',
                           title='Plant-Type Details',
                           plant_type_model=plant_type)


@plant_type_bp.route('/<int:plant_type_id>/delete')
def delete(plant_type_id):
    plant_type = PlantTypeModel.query.get_or_404(plant_type_id)
    db.session.delete(plant_type)
    db.session.commit()
    return redirect(url_for('plant_type.list_all'))


@plant_type_bp.route('/create', methods=['GET', 'POST'])
def create():
    model = PlantTypeModel()
    form = PlantTypeForm(obj=model)
    error = None
    success = None
    if form.validate_on_submit():
        # received valid form
        check_exists = PlantTypeModel.query.filter_by(name=form.name.data).first()
        if check_exists is not None:
            # already exists a plant with given name
            error = 'Cannot create new plant type, as one is already registered with the given name.'
        else:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            success = 'Successfully created a new plant type.'
    return render_template('plant_type/form.html',
                           title='Create Plant-Type',
                           plant_type_form=form,
                           form_endpoint={'endpoint': 'plant_type.create'},
                           back_endpoint={'endpoint': 'plant_type.list_all'},
                           error=error,
                           success=success)


@plant_type_bp.route('/<int:plant_type_id>/edit', methods=['GET', 'POST'])
def edit(plant_type_id):
    plant_type = PlantTypeModel.query.get_or_404(plant_type_id)
    form = PlantTypeForm(obj=plant_type)
    error = None
    success = None
    if form.validate_on_submit():
        # received valid form
        check_exists = PlantTypeModel.query.filter_by(name=form.name.data).first()
        if check_exists is not None and check_exists.id != plant_type_id:
            error = 'There is already another plant type with given name.'
        else:
            form.populate_obj(plant_type)
            db.session.commit()
            success = 'Successfully edited the plant type.'
    return render_template('plant_type/form_edit.html',
                           title='Edit Plant-Type',
                           plant_type_model=plant_type,
                           plant_type_form=form,
                           form_endpoint={'endpoint': 'plant_type.edit',
                                          'plant_type_id': plant_type_id},
                           back_endpoint={'endpoint': 'plant_type.details',
                                          'plant_type_id': plant_type_id},
                           error=error,
                           success=success)
