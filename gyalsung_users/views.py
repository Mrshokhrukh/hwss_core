from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from gyalsung_users.models import GyalsungUserProfile


class SaveGyalsungUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            # Check if user with the provided identity number already exists
            existing_user = GyalsungUserProfile.objects.filter(
                identity_number=data.get("identity_number")
            ).first()

            if existing_user:
                # Update existing user's profile
                existing_user.username = data.get("username")
                existing_user.full_name = data.get("full_name")
                existing_user.gender = data.get("gender")
                existing_user.dob = data.get("dob")
                existing_user.mobile_number = data.get("mobile_number")
                existing_user.ps_add_village = data.get("ps_add_village")
                existing_user.ps_add_gewog = data.get("ps_add_gewog")
                existing_user.ps_add_dzongkhag = data.get("ps_add_dzongkhag")
                existing_user.academy_code = data.get("academy_code")
                existing_user.batch_number = data.get("batch_number")
                existing_user.prev_school = data.get("prev_school")
                existing_user.phq9_score = data.get("phq9_score")
                existing_user.phq9_flag = data.get("phq9_flag")
                existing_user.suicidal_score = data.get("suicidal_score")
                existing_user.suicidal_flag = data.get("suicidal_flag")
                existing_user.gad7_score = data.get("gad7_score")
                existing_user.gad7_flag = data.get("gad7_flag")
                existing_user.tobacco_score = data.get("tobacco_score")
                existing_user.tobacco_flag = data.get("tobacco_flag")
                existing_user.alcohol_score = data.get("alcohol_score")
                existing_user.alcohol_flag = data.get("alcohol_flag")
                existing_user.cannabis_score = data.get("cannabis_score")
                existing_user.cannabis_flag = data.get("cannabis_flag")
                existing_user.cocaine_score = data.get("cocaine_score")
                existing_user.cocaine_flag = data.get("cocaine_flag")
                existing_user.amphetamine_score = data.get("amphetamine_score")
                existing_user.amphetamine_flag = data.get("amphetamine_flag")
                existing_user.inhalants_score = data.get("inhalants_score")
                existing_user.inhalants_flag = data.get("inhalants_flag")
                existing_user.sedatives_score = data.get("sedatives_score")
                existing_user.sedatives_flag = data.get("sedatives_flag")
                existing_user.hallucinogens_score = data.get("hallucinogens_score")
                existing_user.hallucinogens_flag = data.get("hallucinogens_flag")
                existing_user.opioids_score = data.get("opioids_score")
                existing_user.opioids_flag = data.get("opioids_flag")
                existing_user.other_score = data.get("other_score")
                existing_user.other_flag = data.get("other_flag")
                existing_user.other_name = data.get("other_name")
                existing_user.injection_use_score = data.get("injection_use_score")
                existing_user.injection_use_flag = data.get("injection_use_flag")

                existing_user.save()
                return Response(
                    {
                        "message": "User profile updated successfully",
                        "status": status.HTTP_200_OK,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Create a new user profile
                profile = GyalsungUserProfile.objects.create(
                    username=data.get("username"),
                    full_name=data.get("full_name"),
                    gender=data.get("gender"),
                    dob=data.get("dob"),
                    identity_number=data.get("identity_number"),
                    mobile_number=data.get("mobile_number"),
                    ps_add_village=data.get("ps_add_village"),
                    ps_add_gewog=data.get("ps_add_gewog"),
                    ps_add_dzongkhag=data.get("ps_add_dzongkhag"),
                    academy_code=data.get("academy_code"),
                    batch_number=data.get("batch_number"),
                    prev_school=data.get("prev_school"),
                    phq9_score=data.get("phq9_score"),
                    phq9_flag=data.get("phq9_flag"),
                    suicidal_score=data.get("suicidal_score"),
                    suicidal_flag=data.get("suicidal_flag"),
                    gad7_score=data.get("gad7_score"),
                    gad7_flag=data.get("gad7_flag"),
                    tobacco_score=data.get("tobacco_score"),
                    tobacco_flag=data.get("tobacco_flag"),
                    alcohol_score=data.get("alcohol_score"),
                    alcohol_flag=data.get("alcohol_flag"),
                    cannabis_score=data.get("cannabis_score"),
                    cannabis_flag=data.get("cannabis_flag"),
                    cocaine_score=data.get("cocaine_score"),
                    cocaine_flag=data.get("cocaine_flag"),
                    amphetamine_score=data.get("amphetamine_score"),
                    amphetamine_flag=data.get("amphetamine_flag"),
                    inhalants_score=data.get("inhalants_score"),
                    inhalants_flag=data.get("inhalants_flag"),
                    sedatives_score=data.get("sedatives_score"),
                    sedatives_flag=data.get("sedatives_flag"),
                    hallucinogens_score=data.get("hallucinogens_score"),
                    hallucinogens_flag=data.get("hallucinogens_flag"),
                    opioids_score=data.get("opioids_score"),
                    opioids_flag=data.get("opioids_flag"),
                    other_score=data.get("other_score"),
                    other_flag=data.get("other_flag"),
                    other_name=data.get("other_name"),
                    injection_use_score=data.get("injection_use_score"),
                    injection_use_flag=data.get("injection_use_flag"),
                )
                return Response(
                    {
                        "message": "New user profile created successfully",
                        "status": status.HTTP_201_CREATED,
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=500)
