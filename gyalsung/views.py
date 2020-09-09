from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from access.models import CustomUser
from gyalsung.serializers import (
    GyalsungCounselorUserSerializer,
    GyalsungFitUnfitUserSerializer,
)
from gyalsung.models import GyalsungAssessment
from gyalsung.serializers import GyalsungCounselorUserSerializer, GyalsungAssessmentSerializer


class GyalsungCounselorUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_counselors()
        qs.select_related(
            "active_agency",
        )
        return qs


class GyalsungReassessmentTeamUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungCounselorUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        return qs


class GyalsungReassessmentMonitoringUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungFitUnfitUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        qs = qs.filter(gyalsung_screening_status__in=["fit", "unfit"])
        return qs


class GyalsungReassessmentFitUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungFitUnfitUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        qs = qs.filter(gyalsung_screening_status="fit")
        return qs


class GyalsungReassessmentUnfitUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GyalsungFitUnfitUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = CustomUser.objects.for_gyalsung_reassessment_team()
        qs.select_related(
            "active_agency",
        )
        qs = qs.filter(gyalsung_screening_status="unfit")
        return qs


class GyalsungAssessmentViewSet(viewsets.ModelViewSet):
    queryset = GyalsungAssessment.objects.all()
    serializer_class = GyalsungAssessmentSerializer
    permission_classes = [AllowAny]  # You can change this to IsAuthenticated if needed

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Optional filtering by user
        user_id = request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Optional filtering by screening status
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(final_screening_status=status_filter)
        
        # Optional filtering by reassessment screening
        is_reassessment = request.query_params.get('is_reassessment')
        if is_reassessment:
            queryset = queryset.filter(is_reassessment_screening=is_reassessment.lower() == 'true')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get assessments for a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assessments = GyalsungAssessment.objects.filter(user_id=user_id)
        serializer = self.get_serializer(assessments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest_by_user(self, request):
        """Get the latest assessment for a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        latest_assessment = GyalsungAssessment.objects.filter(
            user_id=user_id
        ).order_by('-created_at').first()
        
        if not latest_assessment:
            return Response(
                {"error": "No assessments found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(latest_assessment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def with_counselor_details(self, request):
        """Get assessments with counselor details"""
        assessments = GyalsungAssessment.objects.select_related(
            'user', 'counselor_user', 'reassessment_user'
        ).all()
        
        # Apply filters if provided
        user_id = request.query_params.get('user_id')
        if user_id:
            assessments = assessments.filter(user_id=user_id)
        
        status_filter = request.query_params.get('status')
        if status_filter:
            assessments = assessments.filter(final_screening_status=status_filter)
        
        serializer = self.get_serializer(assessments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_counselor_remarks(self, request, pk=None):
        """Update counselor remarks for a specific assessment"""
        assessment = self.get_object()
        remarks = request.data.get('counselor_remarks')
        
        if remarks is not None:
            assessment.counselor_remarks = remarks
            assessment.save()
            return Response(self.get_serializer(assessment).data)
        
        return Response(
            {"error": "counselor_remarks field is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['patch'])
    def update_reassessment_remarks(self, request, pk=None):
        """Update reassessment remarks for a specific assessment"""
        assessment = self.get_object()
        remarks = request.data.get('reassessment_remarks')
        
        if remarks is not None:
            assessment.reassessment_remarks = remarks
            assessment.save()
            return Response(self.get_serializer(assessment).data)
        
        return Response(
            {"error": "reassessment_remarks field is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['patch'])
    def update_screening_status(self, request, pk=None):
        """Update screening status for a specific assessment"""
        assessment = self.get_object()
        status_value = request.data.get('final_screening_status')
        
        if status_value is not None:
            assessment.final_screening_status = status_value
            assessment.save()
            return Response(self.get_serializer(assessment).data)
        
        return Response(
            {"error": "final_screening_status field is required"},
            status=status.HTTP_400_BAD_REQUEST
        )