from ..forms.plant_type import PlantTypeForm
from ..models.plant_type import PlantTypeModel, db
from flask import Blueprint, render_template


plant_type_bp = Blueprint('plant_type', __name__, url_prefix='/plant_type')


@plant_type_bp.context_processor
def utility_title(title='Plant Type'):
    return dict(title=title)


@plant_type_bp.route('/index')
@plant_type_bp.route('/')
def plant_type_index():
    return render_template('plant_type/index.html')


@plant_type_bp.route('/forms', methods=['GET', 'POST'])
def plant_type_forms():
    model = PlantTypeModel()
    form = PlantTypeForm(obj=model)
    error = None
    success = None

    if form.validate_on_submit():
        # received valid form
        check_exists = PlantTypeModel.query.filter_by(name=form.name.data.lower()).first()
        if check_exists is not None:
            # already exists a plant with given name
            error = 'Cannot create new plant type, as one is already registered with the given name.'
        else:
            form.populate_obj(model)
            db.session.add(model)
            db.session.commit()
            success = 'Successfully created a new plant type.'

    return render_template('plant_type/forms/create.html',
                           title='Create Plant-Type',
                           plant_type_form=form,
                           error=error,
                           success=success)
