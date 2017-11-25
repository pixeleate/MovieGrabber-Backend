from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from . import views

urlpatterns = [


    url(r'^backend/account/favourite$', views.FavouriteApiToggle.as_view(), name='favourite'),
    url(r'^backend/account/autoplay$', views.AutoPlayApiToggle.as_view(), name='AutoPlayApiToggle'),
    url(r'^backend/account/autoplaynext', views.AutoPlayNextApiToggle.as_view(), name='AutoPlayNextApiToggle'),
    url(r'^backend/account/fiverecommended', views.FiveRecommended.as_view(), name='FiveRecommendedApiView'),
    url(r'^backend/account/getFavouries', views.getFavouritesAPI.as_view(), name='getFavouritesApiView'),

    url(r'^backend/account/api-token-auth/', obtain_jwt_token),
    url(r'^backend/account/api-token-verify/', verify_jwt_token),

    url(r'^backend/media/GetNextEpisode', views.GetNextEpisodeAPI.as_view(), name='GetNextEpisodeApi'),
    url(r'^backend/media/GetPrevEpisode', views.GetPrevEpisodeAPI.as_view(), name='GetPrevEpisodeApi'),
    url(r'^backend/media/search', views.ApiSearch.as_view(), name='ApiSearch'),
    url(r'^backend/media/getPopular', views.getPopularAPI.as_view(), name='getPopularAPI'),
    url(r'^backend/media/getDetails', views.getDetailsAPI.as_view(), name='getDetails'),
    url(r'^backend/media/getLinks', views.getLinksAPI.as_view(), name='getLinks'),
    url(r'^backend/media/decodeGFile/(?P<file>.*)', views.decodeGFileAPI.as_view(), name='decodeGFile'),


]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json","html"])
"""url(r'^$', views.home, name='home'),

url(r'^searchaskforapi/', views.post_list, name='post_list'),
url(r'^search_submit/', views.SearchSubmitView.as_view(), name='search-submit'),
url(r'^search_ajax_submit/', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),

url(r'^post/(?P<id>\d+)/(?P<title>.*)/$', views.post_detail, name='post_detail'),
url(r'^link/', views.links.as_view(), name='links'),
url(r'^play/(?P<showid>.*)/(?P<epid>.*)/(?P<streamid>.*)$', views.play, name='plays'),
url(r'^subtitle.vtt/(?P<title>.*)/(?P<no>\d+)/$', views.subtitle, name='subtitle'),
url(r'^browse/$', views.browseTopList.as_view(), name='toplist'),
url(r'^favourites/$', views.browseFavourites.as_view(), name='favourites'),

url(r'^register/$', views.UserFormView.as_view(), name='register'),
url(r'^login/$', views.UserLoginView.as_view(), name='login'),
url(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),
url(r'^account/$', views.UserProfileView.as_view(), name='profile'),
url(r'^account/autoplay$', views.AutoPlaySwitchRedirect.as_view(), name='AutoPlaySwitch'),"""
"""
    url(r'^send_notification/$', views.send_notification, name='send_notification'),
    url(r'^mark_as_read/$', views.mark_as_read, name='mark_as_read'),
"""