from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Movie.objects.all()

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, *args, **kwargs):
        if 'stars' in request.data:
            movie = get_object_or_404(Movie, id=kwargs.get('pk'))
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(
                    user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

            response = {'message': 'its working'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Rating.objects.all()

    def update(self, request, *args, **kwargs):
        response = {'message': 'You can\'t update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You can\'t create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
