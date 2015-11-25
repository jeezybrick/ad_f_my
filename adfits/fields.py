from djangotoolbox.fields import ListField
from bson.objectid import ObjectId
from django.forms import SelectMultiple, MultipleChoiceField


class ModelListField(ListField):
	"""
	No implementation is available for ListField, 
	so ModelListField is custom model field that can 
	be used store to list of ObjectId to mentain foriegnkey relations.

	example author = ModelListField(EmbeddedModelField('Author'))
	Where Author is a model.
	"""

	def __init__(self, embedded_model=None, *args, **kwargs):
		super(ModelListField, self).__init__(*args, **kwargs)
		self._model = embedded_model.embedded_model

	def formfield(self, **kwargs):
		return FormListField(model=self._model, **kwargs)

class ListFieldWidget(SelectMultiple):
  	pass

class FormListField(MultipleChoiceField):
	widget = ListFieldWidget

	def __init__(self, model=None, *args, **kwargs):
		self._model = model
		super(FormListField, self).__init__(*args, **kwargs)
		self.widget.choices = [(ObjectId(i.pk), i) for i in self._model.objects.all()]

	def to_python(self, value):
		return [self._model.objects.get(pk=ObjectId(key)) for key in value]

	def clean(self, value):
		return [ObjectId(key) for key in value]
