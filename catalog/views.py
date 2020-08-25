from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum, Count, Max
from django.views import generic
from django.db.models.signals import pre_save
from django.dispatch import receiver

#--- IMPORT MODELS HERE ---
from catalog.models import PlayerModel, Rd1HoleModel, Rd1SlotModel, Rd1ScoreModel, Rd1StablefordModel, Rd2HoleModel, Rd2SlotModel, Rd2ScoreModel, Rd2StablefordModel, Rd3HoleModel, Rd3SlotModel, Rd3ScoreModel, Rd3StablefordModel, Rd4HoleModel, Rd4SlotModel, Rd4ScoreModel, Rd4StablefordModel, EventEntryModel, LeaderBoardModel, SportsTippingModel,SportsTippingResultsModel, SportsTippingScoreModel, Input_TourDetailsModel, AdminHoleDetails

#--- IMPORT FORMS HERE ---
from catalog.forms import Rd1ScoreForm, Rd2ScoreForm, Rd3ScoreForm, Rd4ScoreForm, SportsTippingForm, MatchReportForm

# --KEY INPUTS-- #
# Add tour name
tour_name = 'The Jersey Jaunt'
# Add Location and Date details
location_date = 'Crystal Springs, October 23-25'
# Calculations to format title
title_list = tour_name.split()
first_part = title_list[0:2]
second_part = title_list[-1]
tour_name_top_line = ' '.join(first_part)
tour_name_highlight = ''.join(second_part)

#--- CREATE VIEWS HERE ---
# LOGIN
def login (request):
    """View function for login of site."""

    # Define views here
    context = {
    'tour_name': tour_name,
    'tour_name_top_line': tour_name_top_line,
    'tour_name_highlight': tour_name_highlight,
    'location_date': location_date,

    }
    return render(request, 'login.html', context=context)

# LANDING PAGE
def landingpage (request):
    """View function for login of site."""
    # Define views here
    context = {}
    return render(request, 'landingpage.html', context=context)

# FULL LEADERBOARD
def fullleaderboard (request):
    """Define function for leaderboard view"""
    # Define views here
    score_submit = EventEntryModel.objects.exclude(winner__isnull=True).count()
    active_players = PlayerModel.objects.all()

    loaded_points = list(EventEntryModel.objects.aggregate(Sum('points')).values())[0]
    awarded_points = list(EventEntryModel.objects.exclude(winner__isnull=True).aggregate(Sum('points')).values())[0]

    context = {
    'score_submit': score_submit,
    'active_players': active_players,
    'loaded_points': loaded_points,
    'awarded_points': awarded_points,
    'tour_name_top_line': tour_name_top_line,
    'tour_name_highlight': tour_name_highlight,
    }
    return render(request, 'fullLeaderboard.html', context=context)

# SCORE ENTRY MENU
def scoringpage (request):
    """View function for scoring page."""

    #pick up defined inputs from AdminHoleDetails to populate round
    #Round 1
    try:
        rd1_name = AdminHoleDetails.objects.get(roundNum=1).courseName
    except:
        rd1_name = "Course TBD"
    #Round 2
    try:
        rd2_name = AdminHoleDetails.objects.get(roundNum=2).courseName
    except:
        rd2_name = "Course TBD"
    #Round 3
    try:
        rd3_name = AdminHoleDetails.objects.get(roundNum=3).courseName
    except:
        rd3_name = "Course TBD"


    context = {
        'rd1_name': rd1_name,
        'rd2_name': rd2_name,
        'rd3_name': rd3_name,
    }

    return render(request, 'scoringPage.html', context=context)

def tourdetails(request):
    """Landing page for tour details"""

    try:
        map_link = Input_TourDetailsModel.objects.get(tour_name=tour_name).map_link
    except:
        map_link = ""

    context = {
        'map_link': map_link,

    }

    return render(request, 'tourDetails.html', context=context)

## --- START ROUND 1 --- ##

class rd1holelist (generic.ListView):
    """Create list of holes"""
    model = Rd1HoleModel
    template_name = 'rd1HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd1HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd1HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd1HoleModel.objects.filter(tussle__isnull=False)

        try:
            scorecard_link = AdminHoleDetails.objects.get(roundNum=1).scorecardLink
        except:
            scorecard_link = ""

        context['scorecard_link'] = scorecard_link
        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd1holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd1HoleModel.objects.get(pk=pk).number
    hole_index = Rd1HoleModel.objects.get(pk=pk).index
    hole_par = Rd1HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd1HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd1HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd1HoleModel.objects.get(number=pk)
    hole_tussle = Rd1HoleModel.objects.get(pk=pk).tussle
    try:
        tussle_name = AdminHoleDetails.objects.get(roundNum=1).tussleName
    except:
        tussle_name = ""

    #Count active players for dynamic loading
    active_players = Rd1SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd1SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd1SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd1SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd1SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd1SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd1SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd1SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd1SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd1SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd1SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd1SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd1SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd1ScoreForm(request.POST)
        try:
            instance = Rd1ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('rd1holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd1holelist')
    else:
        try:
            form = Rd1ScoreForm(instance=get_object_or_404(Rd1ScoreModel,hole=selected_hole))
        except:
            form = Rd1ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        'tussle_name': tussle_name,
        }

    return render(request, 'rd1HoleDetail.html', context=context)

def rd1leaderboard(request):
    """Create leaderboard view for Round1"""

    #Add views
    playing_players = Rd1SlotModel.objects.filter(player_name__isnull=False)

    endurance_leader = Rd1SlotModel.objects.aggregate(Max('endurance_score'))

    #Add context
    context = {
        'playing_players': playing_players,
        'endurance_leader': endurance_leader,
        }

    return render(request, 'rd1Leaderboard.html', context=context)

# ## -- END ROUND 1 -- ##

## -- START ROUND 2 -- ##
class rd2holelist (generic.ListView):
    """Create list of holes"""
    model = Rd2HoleModel
    template_name = 'rd2HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd2HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd2HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd2HoleModel.objects.filter(tussle__isnull=False)
        try:
            scorecard_link = AdminHoleDetails.objects.get(roundNum=2).scorecardLink
        except:
            scorecard_link = ""

        context['scorecard_link'] = scorecard_link

        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd2holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd2HoleModel.objects.get(pk=pk).number
    hole_index = Rd2HoleModel.objects.get(pk=pk).index
    hole_par = Rd2HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd2HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd2HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd2HoleModel.objects.get(number=pk)
    hole_tussle = Rd1HoleModel.objects.get(pk=pk).tussle
    try:
        tussle_name = AdminHoleDetails.objects.get(roundNum=2).tussleName
    except:
        tussle_name = ""

    #Count active players for dynamic loading
    active_players = Rd2SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd2SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd2SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd2SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd2SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd2SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd2SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd2SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd2SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd2SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd2SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd2SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd2SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd2ScoreForm(request.POST)
        try:
            instance = Rd2ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('rd2holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd2holelist')
    else:
        try:
            form = Rd2ScoreForm(instance=get_object_or_404(Rd2ScoreModel,hole=selected_hole))
        except:
            form = Rd2ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        'tussle_name': tussle_name,
        }

    return render(request, 'rd2HoleDetail.html', context=context)

def rd2leaderboard(request):
    """Create leaderboard view for Round2"""

    #Add views
    playing_players = Rd2SlotModel.objects.filter(player_name__isnull=False)

    #Add context
    context = {
        'playing_players': playing_players,
        }

    return render(request, 'rd2Leaderboard.html', context=context)

## --END ROUND 2 -- ##

## START ROUND 3 -- ##
class rd3holelist (generic.ListView):
    """Create list of holes"""
    model = Rd3HoleModel
    template_name = 'rd3HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd3HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd3HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd3HoleModel.objects.filter(tussle__isnull=False)
        try:
            scorecard_link = AdminHoleDetails.objects.get(roundNum=3).scorecardLink
        except:
            scorecard_link = ""

        context['scorecard_link'] = scorecard_link

        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd3holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd3HoleModel.objects.get(pk=pk).number
    hole_index = Rd3HoleModel.objects.get(pk=pk).index
    hole_par = Rd3HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd3HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd3HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd3HoleModel.objects.get(number=pk)
    hole_tussle = Rd1HoleModel.objects.get(pk=pk).tussle
    try:
        tussle_name = AdminHoleDetails.objects.get(roundNum=3).tussleName
    except:
        tussle_name = ""

    #Count active players for dynamic loading
    active_players = Rd3SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd3SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd3SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd3SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd3SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd3SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd3SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd3SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd3SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd3SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd3SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd3SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd3SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd3ScoreForm(request.POST)
        try:
            instance = Rd3ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('rd3holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd3holelist')
    else:
        try:
            form = Rd3ScoreForm(instance=get_object_or_404(Rd3ScoreModel,hole=selected_hole))
        except:
            form = Rd3ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        'tussle_name': tussle_name,
        }

    return render(request, 'rd3HoleDetail.html', context=context)

def rd3leaderboard(request):
    """Create leaderboard view for Round3"""

    #Add views
    playing_players = Rd3SlotModel.objects.filter(player_name__isnull=False)

    #Add context
    context = {
        'playing_players': playing_players,
        }

    return render(request, 'rd3Leaderboard.html', context=context)

## -- END ROUND 3 -- ##

## -- TIPPING
def entertips(request):
    """Create view for tips entry view"""

    #Add views
    if request.method == 'POST':
        form = SportsTippingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('tipresults')

    else:
        form = SportsTippingForm()

    context = {
        'tour_name': tour_name,
        'form': form,
        }

    return render(request, 'enterSportsTips.html', context=context)

# -- TIPPING RESULTS
def tipresults(request):
    """Redirect page for input and show results"""
    #Basic counts and definitions
    recordedtips = SportsTippingScoreModel.objects.all()

    try:
        results = SportsTippingResultsModel.objects.get(name="result")

        if results:
            if results.result1 == "NOT_COMPLETE":
                num_games1 = 0
            else:
                num_games1 = 1
            if results.result2 == "NOT_COMPLETE":
                num_games2 = 0
            else:
                num_games2 = 1
            if results.result3 == "NOT_COMPLETE":
                num_games3 = 0
            else:
                num_games3 = 1
            if results.result4 == "NOT_COMPLETE":
                num_games4 = 0
            else:
                num_games4 = 1
            if results.result5 == "NOT_COMPLETE":
                num_games5 = 0
            else:
                num_games5 = 1
            if results.result6 == "NOT_COMPLETE":
                num_games6 = 0
            else:
                num_games6 = 1
            if results.result7 == "NOT_COMPLETE":
                num_games7 = 0
            else:
                num_games7 = 1
            if results.result8 == "NOT_COMPLETE":
                num_games8 = 0
            else:
                num_games8 = 1
            if results.result9 == "NOT_COMPLETE":
                num_games9 = 0
            else:
                num_games9 = 1
            if results.result10 == "NOT_COMPLETE":
                num_games10 = 0
            else:
                num_games10 = 1

            num_games = num_games1 +num_games2 +num_games3 +num_games4 +num_games5 +num_games6 +num_games7 +num_games8 +num_games9 +num_games10

        else:
            num_games = 0

    except:
        num_games = 0

    context = {
        'tour_name': tour_name,
        'recordedtips': recordedtips,
        'num_games': num_games,
        }

    return render(request, 'tipResults.html', context=context)

def entersocial(request):
    """Create view for social entry view"""

    if request.method == 'POST':
        if 'friday' in request.POST:
            fridayform = FridaySocialForm(request.POST, prefix='friday')
            if fridayform.is_valid():
                post = fridayform.save(commit=False)
                post.save()
                return redirect('landingpage')
                saturdayform = SaturdaySocialForm(prefix='saturday')

        elif 'saturday' in request.POST:
            saturdayform = SaturdaySocialForm(request.POST, prefix='saturday')
            if saturdayform.is_valid():
                post = saturdayform.save(commit=False)
                post.save()
                return redirect('landingpage')
                fridayform = FridaySocialForm(prefix='friday')
    else:
        fridayform = FridaySocialForm(prefix='friday')
        saturdayform = SaturdaySocialForm(prefix='saturday')

    context = {
        #'fridayform': fridayform,
        'saturdayform': saturdayform,
        'fridayform': fridayform,
        }

    return render(request, 'enterSocial.html', context=context)

## -- Tour players
def tourplayers(request):
    """Landing page for tour details"""
    active_players = PlayerModel.objects.order_by('number')

    context = {
        'tour_name': tour_name,
        'active_players': active_players,
        }

    return render(request, 'tourPlayers.html', context=context)

## - Tour agenda
def touragenda(request):
    """Landing page for tour details"""
    # active_events = TourAgendaModel.objects.order_by('number')
    # friday_events = TourAgendaModel.objects.all().filter(day='FRIDAY')
    # saturday_events = TourAgendaModel.objects.all().filter(day='SATURDAY')
    # sunday_events = TourAgendaModel.objects.all().filter(day='SUNDAY')

    try:
        points_link = Input_TourDetailsModel.objects.get(tour_name=tour_name).points_link
    except:
         points_link = ""

    context = {
        'tour_name': tour_name,
        'points_link': points_link,
        # 'active_events': active_events,
        # 'friday_events': friday_events,
        # 'saturday_events': saturday_events,
        # 'sunday_events': sunday_events,
        }

    return render(request, 'tourAgenda.html', context=context)

def playerdetail (request,name):
    """View function showing individual player's results"""

    #Basic player details
    player_image = PlayerModel.objects.get(name=name).image
    player_HC = PlayerModel.objects.get(name=name).HC
    player_highfinish = PlayerModel.objects.get(name=name).highfinish
    player_tournum = PlayerModel.objects.get(name=name).tournum
    player_totalpoints = LeaderBoardModel.objects.get(player=name).overall_total
    player_totalrank = LeaderBoardModel.objects.filter(overall_total__gt=player_totalpoints).count() + 1


    target_holes = 10 #Change to 10 in production

    ##START ROUND 1 CALCULATIONS -->
    #Trigger to show score only when round finished
    try:
        rd1holes_played = Rd1SlotModel.objects.get(player_name__name=name).player_holesplayed
        if rd1holes_played is None:
            rd1holes_played = 0
        else:
            rd1holes_played = Rd1SlotModel.objects.get(player_name__name=name).player_holesplayed
    except:
        rd1holes_played = 0



    #Rd1 Player golf score & rank
    if rd1holes_played >= target_holes:
        rd1golf_score = Rd1SlotModel.objects.get(player_name__name=name).player_score
        rd1golf_scoreRank = Rd1SlotModel.objects.filter(player_score__lt=rd1golf_score).count() + 1
        rd1golf_stbl = Rd1SlotModel.objects.get(player_name__name=name).player_stbl
        rd1golf_stblRank = Rd1SlotModel.objects.filter(player_stbl__gt=rd1golf_stbl).count() + 1
    else:
        rd1golf_score = "-"
        rd1golf_scoreRank= "n/a"
        rd1golf_stbl = "-"
        rd1golf_stblRank= "n/a"

    #Rd1PlayerPoints
    try:
        rd1golf_points = LeaderBoardModel.objects.get(player=name).rd1_golf
    except:
        rd1golf_points = "-"
    try:
        rd1golf_rank = LeaderBoardModel.objects.filter(rd1_golf__gt=rd1golf_points).count() + 1
    except:
        rd1golf_rank = "-"
    try:
        rd1ctpld_points = LeaderBoardModel.objects.get(player=name).rd1_ctpld
    except:
        rd1ctpld_points = "-"
    try:
        rd1ctpld_rank = LeaderBoardModel.objects.filter(rd1_ctpld__gt=rd1ctpld_points).count() + 1
    except:
        rd1ctpld_rank = "-"
    try:
        rd1bonus_points = LeaderBoardModel.objects.get(player=name).rd1_bonus
    except:
        rd1bonus_points = "-"
    try:
        rd1bonus_rank = LeaderBoardModel.objects.filter(rd1_bonus__gt=rd1bonus_points).count() + 1
    except:
        rd1bonus_rank = "-"
    try:
        rd1total_points = rd1golf_points + rd1ctpld_points + rd1bonus_points
    except:
        rd1total_points = "-"
    try:
        rd1total_rank = LeaderBoardModel.objects.filter(rd1_total__gt=rd1total_points).count() + 1
    except:
        rd1total_rank = "-"

    try:
        round1overall_points = list(LeaderBoardModel.objects.aggregate(Sum('rd1_total')).values())[0]
    except:
        round1overall_points = 0


    ##START ROUND 2 CALCULATIONS -->
    #Trigger to show score only when round finished
    try:
        rd2holes_played = Rd2SlotModel.objects.get(player_name__name=name).player_holesplayed
        if rd2holes_played is None:
            rd2holes_played = 0
        else:
            rd2holes_played = Rd2SlotModel.objects.get(player_name__name=name).player_holesplayed
    except:
        rd2holes_played = 0

    #Rd2 Player golf score & rank
    if rd2holes_played >= target_holes:
        rd2golf_score = Rd2SlotModel.objects.get(player_name__name=name).player_score
        rd2golf_scoreRank = Rd2SlotModel.objects.filter(player_score__lt=rd2golf_score).count() + 1
        rd2golf_stbl = Rd2SlotModel.objects.get(player_name__name=name).player_stbl
        rd2golf_stblRank = Rd2SlotModel.objects.filter(player_stbl__gt=rd2golf_stbl).count() + 1
    else:
        rd2golf_score = "-"
        rd2golf_scoreRank= "n/a"
        rd2golf_stbl = "-"
        rd2golf_stblRank= "n/a"

    #Rd2PlayerPoints
    try:
        rd2golf_points = LeaderBoardModel.objects.get(player=name).rd2_golf
    except:
        rd2golf_points = "-"
    try:
        rd2golf_rank = LeaderBoardModel.objects.filter(rd2_golf__gt=rd2golf_points).count() + 1
    except:
        rd2golf_rank = "-"
    try:
        rd2ctpld_points = LeaderBoardModel.objects.get(player=name).rd2_ctpld
    except:
        rd2ctpld_points = "-"
    try:
        rd2ctpld_rank = LeaderBoardModel.objects.filter(rd2_ctpld__gt=rd2ctpld_points).count() + 1
    except:
        rd2ctpld_rank = "-"
    try:
        rd2bonus_points = LeaderBoardModel.objects.get(player=name).rd2_bonus
    except:
        rd2bonus_points = "-"
    try:
        rd2bonus_rank = LeaderBoardModel.objects.filter(rd2_bonus__gt=rd2bonus_points).count() + 1
    except:
        rd2bonus_rank = "-"
    try:
        rd2total_points = rd2golf_points + rd2ctpld_points + rd2bonus_points
    except:
        rd2total_points = "-"
    try:
        rd2total_rank = LeaderBoardModel.objects.filter(rd2_total__gt=rd2total_points).count() + 1
    except:
        rd2total_rank = "-"

    try:
        round2overall_points = list(LeaderBoardModel.objects.aggregate(Sum('rd2_total')).values())[0]
    except:
        round2overall_points = 0

    ##START ROUND 3 CALCULATIONS -->
    #Trigger to show score only when round finished
    try:
        rd3holes_played = Rd3SlotModel.objects.get(player_name__name=name).player_holesplayed
        if rd3holes_played is None:
            rd3holes_played = 0
        else:
            rd3holes_played = Rd3SlotModel.objects.get(player_name__name=name).player_holesplayed
    except:
        rd3holes_played = 0

    #Rd3 Player golf score & rank
    if rd3holes_played >= target_holes:
        rd3golf_score = Rd3SlotModel.objects.get(player_name__name=name).player_score
        rd3golf_scoreRank = Rd3SlotModel.objects.filter(player_score__lt=rd2golf_score).count() + 1
        rd3golf_stbl = Rd3SlotModel.objects.get(player_name__name=name).player_stbl
        rd3golf_stblRank = Rd3SlotModel.objects.filter(player_stbl__gt=rd2golf_stbl).count() + 1
    else:
        rd3golf_score = "-"
        rd3golf_scoreRank= "n/a"
        rd3golf_stbl = "-"
        rd3golf_stblRank= "n/a"

    #Rd2PlayerPoints
    try:
        rd3golf_points = LeaderBoardModel.objects.get(player=name).rd3_golf
    except:
        rd3golf_points = "-"
    try:
        rd3golf_rank = LeaderBoardModel.objects.filter(rd3_golf__gt=rd3golf_points).count() + 1
    except:
        rd3golf_rank = "-"
    try:
        rd3ctpld_points = LeaderBoardModel.objects.get(player=name).rd3_ctpld
    except:
        rd3ctpld_points = "-"
    try:
        rd3ctpld_rank = LeaderBoardModel.objects.filter(rd3_ctpld__gt=rd3ctpld_points).count() + 1
    except:
        rd3ctpld_rank = "-"
    try:
        rd3bonus_points = LeaderBoardModel.objects.get(player=name).rd3_bonus
    except:
        rd3bonus_points = "-"
    try:
        rd3bonus_rank = LeaderBoardModel.objects.filter(rd3_bonus__gt=rd3bonus_points).count() + 1
    except:
        rd3bonus_rank = "-"
    try:
        rd3total_points = rd3golf_points + rd3ctpld_points + rd3bonus_points
    except:
        rd3total_points = "-"
    try:
        rd3total_rank = LeaderBoardModel.objects.filter(rd3_total__gt=rd3total_points).count() + 1
    except:
        rd3total_rank = "-"

    try:
        round3overall_points = list(LeaderBoardModel.objects.aggregate(Sum('rd3_total')).values())[0]
    except:
        round3overall_points = 0

    ##START OTHER_SCORES CALCULATIONS -->

    #Other Player Points
    try:
        social_points = LeaderBoardModel.objects.get(player=name).social
    except:
        social_points = "-"
    try:
        social_rank = LeaderBoardModel.objects.filter(social__gt=social_points).count() + 1
    except:
        social_rank = "-"
    try:
        bestdressed_points = LeaderBoardModel.objects.get(player=name).best_dressed
    except:
        bestdressed_points = "-"
    try:
        bestdressed_rank = LeaderBoardModel.objects.filter(best_dressed__gt=bestdressed_points).count() + 1
    except:
        bestdressed_rank = "-"
    try:
        tipping_points = LeaderBoardModel.objects.get(player=name).tipping
    except:
        tipping_points = "-"
    try:
        tipping_rank = LeaderBoardModel.objects.filter(tipping__gt=tipping_points).count() + 1
    except:
        tipping_rank = "-"
    try:
        othertotal_points = social_points + bestdressed_points + tipping_points
    except:
        othertotal_points = "-"
    try:
        othertotal_rank = LeaderBoardModel.objects.filter(other_total__gt=othertotal_points).count() + 1
    except:
        othertotal_rank = "-"

    try:
        otheroverall_points = list(LeaderBoardModel.objects.aggregate(Sum('other_total')).values())[0]
    except:
        otheroverall_points = 0

## == END SCORING CALCS ==

    context ={
    'name': name,
    'player_image': player_image,
    'player_HC': player_HC,
    'player_highfinish': player_highfinish,
    'player_tournum': player_tournum,
    'player_totalpoints': player_totalpoints,
    'player_totalrank': player_totalrank,
    'rd1golf_score': rd1golf_score,
    'rd1golf_stbl': rd1golf_stbl,
    'rd1golf_scoreRank': rd1golf_scoreRank,
    'rd1golf_stblRank': rd1golf_stblRank,
    'rd1golf_points': rd1golf_points,
    'rd1golf_rank': rd1golf_rank,
    'rd1ctpld_points': rd1ctpld_points,
    'rd1ctpld_rank': rd1ctpld_rank,
    'rd1bonus_points': rd1bonus_points,
    'rd1bonus_rank': rd1bonus_rank,
    'rd1total_points': rd1total_points,
    'rd1total_rank': rd1total_rank,
    'round1overall_points': round1overall_points,
    'rd2golf_score': rd2golf_score,
    'rd2golf_stbl': rd2golf_stbl,
    'rd2golf_scoreRank': rd2golf_scoreRank,
    'rd2golf_stblRank': rd2golf_stblRank,
    'rd2golf_points': rd2golf_points,
    'rd2golf_rank': rd2golf_rank,
    'rd2ctpld_points': rd2ctpld_points,
    'rd2ctpld_rank': rd2ctpld_rank,
    'rd2bonus_points': rd2bonus_points,
    'rd2bonus_rank': rd2bonus_rank,
    'rd2total_points': rd2total_points,
    'rd2total_rank': rd2total_rank,
    'round2overall_points': round2overall_points,
    'rd3golf_score': rd3golf_score,
    'rd3golf_stbl': rd3golf_stbl,
    'rd3golf_scoreRank': rd3golf_scoreRank,
    'rd3golf_stblRank': rd3golf_stblRank,
    'rd3golf_points': rd3golf_points,
    'rd3golf_rank': rd3golf_rank,
    'rd3ctpld_points': rd3ctpld_points,
    'rd3ctpld_rank': rd3ctpld_rank,
    'rd3bonus_points': rd3bonus_points,
    'rd3bonus_rank': rd3bonus_rank,
    'rd3total_points': rd3total_points,
    'rd3total_rank': rd3total_rank,
    'round3overall_points': round3overall_points,
    'social_points': social_points,
    'social_rank': social_rank,
    'bestdressed_points': bestdressed_points,
    'bestdressed_rank': bestdressed_rank,
    'tipping_points': tipping_points,
    'tipping_rank': tipping_rank,
    'othertotal_points': othertotal_points,
    'othertotal_rank': othertotal_rank,
    'otheroverall_points': otheroverall_points,

    }

    return render(request, 'playerDetail.html', context=context)


def matchreports(request):
    """View results and generate match reports including text to speech file"""

#SET ROUND USING FORM
    print("ROUNDNUMBER")
    round_number = {}
    polly_voice = {}

    if request.method =='POST':
         form = MatchReportForm(request.POST)
         if form.is_valid():
             round_number = form.round_select(request).roundNum
             polly_voice = form.voice_select(request)
    else:
          form = MatchReportForm()

    print(round_number)

## ERROR HANDLING IF NO ROUND DETAILS SELECTED
    try:
        if round_number == 1:
            select_slot_model = Rd1SlotModel
            select_score_model = Rd1ScoreModel
            select_hole_model = Rd1HoleModel
        elif round_number == 2:
            select_slot_model = Rd2SlotModel
            select_score_model = Rd2ScoreModel
            select_hole_model = Rd2HoleModel
        elif round_number == 3:
            select_slot_model = Rd3SlotModel
            select_score_model = Rd3ScoreModel
            select_hole_model = Rd3HoleModel
        # else:
        #     select_slot_model = Rd3SlotModel
        #     select_score_model = Rd3ScoreModel
        #     select_hole_model = Rd3HoleModel

    # GET ROUND SCORE DETAILS (looped in html template)
        round_details = select_slot_model.objects.filter(player_holesplayed__gt=0).order_by('-player_rankscore')

    # CTP DETAILS
    #Create list of CTP holes selected when creating round
        ctp_holes = []
        hole_details = select_hole_model.objects.filter(CTP__gt=0)
        for ctp in hole_details:
            ctp_holes.append(ctp.number)

    #Create list of CTP holes in play in selected round
        ctp_details = select_score_model.objects.all()

        ctp_inplay = []
        for hole in ctp_details:
            ctp_inplay.append(hole.hole.number)

    #Match winners to selected holes
        ctp_winners = []
        for hole in ctp_details:
            for ctp in ctp_holes:
                if hole.hole.number == ctp:
                    try:
                        ctp_winners.append(select_score_model.objects.get(hole=hole.hole.number).ctp.name)
                    except:
                        ctp_winners.append("No winner")

        print(ctp_holes)
        print(ctp_winners)

        zipped_ctp = list(zip(ctp_holes, ctp_winners))

    # LD DETAILS
    #Create list of LD holes selected when creating round
        ld_holes = []
        hole_details = select_hole_model.objects.filter(LD__gt=0)
        for ld in hole_details:
            ld_holes.append(ld.number)

    #Create list of LD holes in play in selected round
        ld_details = select_score_model.objects.all()

        ld_inplay = []
        for hole in ld_details:
            ld_inplay.append(hole.hole.number)

    #Match winners to selected holes
        ld_winners = []
        for hole in ld_details:
            for ld in ld_holes:
                if hole.hole.number == ld:
                    try:
                        ld_winners.append(select_score_model.objects.get(hole=hole.hole.number).ld.name)
                    except:
                        ld_winners.append("No-one")

        print(ld_holes)
        print(ld_winners)

        zipped_ld = list(zip(ld_holes, ld_winners))

    # Get tussle winner
        tussle_results = select_slot_model.objects.filter(player_name__isnull=False).order_by('-tussle_score', 'player_score')

    # GENERATE MATCH REPORT TEXT
        import random
        adjective_list = ['saucy', 'sizzling', 'breathtaking']
        active_verb_list = ['monstered', 'obliterated']
        old_saying_list = ['Stone the Crows', 'Sweet Jesus']
        animals_list = ['dogs', 'cats', 'rhinos', 'giraffes']
        event_list = ['dinner date', 'dentist appointment']
        golf_saying_list = ['Drive for show, putt for dough', 'Got to be in it to win it']
        adverb_list = ['cheerily', 'idiotically', 'non-sensically', 'sulkily']


        player_list = []
        active_players = PlayerModel.objects.all()
        for player in active_players:
            player_list.append(player.name)

        random_adjective1 = random.choice(adjective_list)
        random_player1 = random.choice(player_list)
        random_old_saying1 = random.choice(old_saying_list)
        random_animals1 = random.choice(animals_list)
        random_event1 = random.choice(event_list)
        active_verb1 = random.choice(active_verb_list)
        random_player2 = random.choice(player_list)
        golf_saying1 = random.choice(golf_saying_list)
        adverb1 = random.choice(adverb_list)

        try:
            ld_winner1 = ld_winners[0]
            ld_hole1 = ld_holes[0]
        except:
            ld_winner1 = "no-one"
            ld_hole1 = "-"

        #Report text
        report_text = """
            Welcome to the Match Report for round {}.

            The day's play could really be summed up in just one word: {}.

            As {} was heard to exclaim as he topped another seven iron at the driving range pre-round: '{}, it's going to be {} out there today!'

            And {} it was. From the first tee shot to the last putt, the players jostled for leaderboard dominance like a group of {} late to a {}.

            But just as in the animal kingdom, it wasn't long before a pack leader presented himself, this time in the form of {}, who stepped up to the tee on hole {} and {} his drive up the fairway to take out the first longest drive prize of the day.

            '{}' said {}, {}, as he watched the ball disappear into the distance.
        """.format(
            round_number,
            random_adjective1,
            random_player1,
            random_old_saying1,
            random_adjective1,
            random_adjective1,
            random_animals1,
            random_event1,
            ld_winner1,
            ld_hole1,
            active_verb1,
            golf_saying1,
            random_player2,
            adverb1
            )

##RESULTS IF NO ROUND DETAILS SELECTED
    except:
        round_details = None
        zipped_ctp = None
        zipped_ld = None
        tussle_results = None
        report_text = None
        polly_voice = "Amy"

    request.session['polly_voice'] = polly_voice
    request.session['report_text'] = report_text
    request.session['round_number'] = round_number

    context = {
        'form': form,
        'round_details': round_details,
        'zipped_ctp': zipped_ctp,
        'zipped_ld': zipped_ld,
        'tussle_results': tussle_results,
        'report_text': report_text,
        # 'ctp_holes': ctp_holes,
        # 'ctp_winners': ctp_winners,
        # 'player_1': player_1,
        # 'ctp_1': ctp_1,
    }

    return render(request, 'matchreports.html', context=context)

def matchreportsfile(request):

    polly_voice = request.session['polly_voice']
    report_text = request.session['report_text']
    round_number = request.session['round_number']

    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
    from contextlib import closing
    import os
    import sys
    import subprocess
    from tempfile import gettempdir

    # Define session
    polly_client = boto3.Session().client('polly',region_name='us-east-1')

    # Function to create audio file
    def createReport(text, round_number, voice):
        #Define Polly synthesize_speech request
        response = polly_client.synthesize_speech(
                        VoiceId=polly_voice,
                        OutputFormat='mp3',
                        Text = text,
                        Engine='standard')

        #Create and save audio file
        filename = 'RoundReport-' + str(round_number) + '-' + voice
        file = open(filename, 'wb')
        file.write(response['AudioStream'].read())
        file.close()

        from os import environ as CONFIG
        AWS_ACCESS_KEY_ID = CONFIG['AWS_ACCESS_KEY_ID']
        AWS_SECRET_ACCESS_KEY = CONFIG['AWS_SECRET_ACCESS_KEY']
        AWS_STORAGE_BUCKET_NAME = CONFIG['AWS_STORAGE_BUCKET_NAME']

        s3_filename = filename + '.mp3'

        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(filename, AWS_STORAGE_BUCKET_NAME, s3_filename)
        except ClientError as e:
            logging.error(e)
            return False
        return True

# CALL CREATE REPORT FUNCTION TO GENERATE REPORT
    createReport(report_text, round_number, polly_voice)

    context={}

    return render(request, 'matchreportsfile.html', context=context)
