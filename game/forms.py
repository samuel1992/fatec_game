from django import forms

from game.models import Answer, Choice


class AnswerForm(forms.ModelForm):
    def __init__(self, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        if question:
            choices = [(c.id, c) for c in question.choices.all()]
            self.fields['choice'] = forms.ChoiceField(choices=tuple(choices),
                                                      widget=forms.RadioSelect)

    class Meta:
        model = Answer
        fields = ('choice', )

    def is_valid(self):
        valid = super(AnswerForm, self).is_valid()

        return valid and self.instance.choice.correct
