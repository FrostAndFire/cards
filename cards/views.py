from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Card, Rating
from .forms import RateForm

# index view

def index(request):
    cards = Card.objects.all()
    context = {
        'data': zip(
            [card.name for card in cards],
            [card.id for card in cards]
            )}
    return render(request, 'index.html', context)

# card view

def card(request, card_id):

    card = get_object_or_404(Card, id=card_id)
    form = RateForm()
    context = {
        'id': card.id,
        'name': card.name,
        'content': card.content,
        'avg_rating': card.avg_rating,
        'form': form,
    }

    if request.method == "GET":
        
        return render(request, 'card.html', context)
    
    elif request.method == "POST":
        
        form = RateForm(request.POST)
        
        if form.is_valid():
            try:
                rate = Rating.objects.get(
                    card=card_id,
                    user=request.user
                    )
                rate.rating = form.cleaned_data['rating']
                
                rate.save()
                
            except Rating.DoesNotExist:    
                rate = Rating(
                    card = Card.objects.get(id=card_id),
                    user = request.user,
                    rating = form.cleaned_data['rating'],
                )

                rate.save()

        all_rates = Rating.objects.filter(card=card_id)
        avg = all_rates.aggregate(Avg('rating'))['rating__avg']
        card.avg_rating = avg

        card.save()
            
        return render(request, 'ratings/card.html', context)
