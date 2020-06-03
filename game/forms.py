from django import forms

from game.models import Answer, Choice


class AnswerForm(forms.ModelForm):
    def __init__(self, question, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        choices = [(c.id, c) for c in question.choices.all()]
        self.fields['choice'] = forms.ChoiceField(choices=tuple(choices),
                                                  widget=forms.RadioSelect)

    class Meta:
        model = Answer
        fields = ('choice', )

    def is_valid(self):
        import pdb;pdb.set_trace()
        valid = super(AnswerForm, self).is_valid()


        if not valid:
            return valid

        choice = Choice.objects.get(id=self.cleaned_data['choice'])
        self.instance.choice = choice

        return True
