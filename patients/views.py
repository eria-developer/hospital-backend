from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(APIView):
    """
    API view to list all patients or create a new patient.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all patients.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing a list of serialized patient objects.
                      Status code 200 OK on success.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new patient.

        Parameters:
            request (Request): The HTTP request object containing the patient data in JSON format.
                              Expected fields:
                              - first_name (str): The patient's first name (required, max 100 characters).
                              - last_name (str): The patient's last name (required, max 100 characters).
                              - date_of_birth (date): The patient's date of birth in YYYY-MM-DD format (required, not in future).
                              - gender (str): The patient's gender ('M', 'F', or 'O') (required).
                              - medical_record_number (str): The unique medical record number (required, max 50 characters, unique).
                              - phone (str): The patient's phone number (required, max 15 characters, e.g., +1234567890).
                              - email (str): The patient's email address (optional, valid email format).
                              - address (str): The patient's address (optional, can be blank).
                              - emergency_contact_phone (str): The phone number of the emergency contact (optional, max 15 characters, e.g., +1234567890).
                              - is_active (bool): Whether the patient is active (optional, default true).

        Returns:
            Response: A JSON response containing the serialized patient object on success with status code 201 Created.
                      If the input data is invalid (e.g., duplicate medical record number or invalid phone), returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    """
    API view to retrieve, update, or delete a specific patient.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve a patient by its primary key.

        Parameters:
            pk (int): The primary key of the patient.

        Returns:
            Patient: The patient object if found, otherwise None.
        """
        try:
            return Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a patient by its ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the patient to retrieve.

        Returns:
            Response: A JSON response containing the serialized patient object with status code 200 OK.
                      If the patient is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        patient = self.get_object(pk)
        if patient is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a patient by its ID.

        Parameters:
            request (Request): The HTTP request object containing the updated patient data in JSON format.
                              Expected fields (partial updates allowed):
                              - first_name (str): The patient's first name (max 100 characters).
                              - last_name (str): The patient's last name (max 100 characters).
                              - date_of_birth (date): The patient's date of birth in YYYY-MM-DD format (not in future).
                              - gender (str): The patient's gender ('M', 'F', or 'O').
                              - medical_record_number (str): The unique medical record number (max 50 characters, unique).
                              - phone (str): The patient's phone number (max 15 characters, e.g., +1234567890).
                              - email (str): The patient's email address (valid email format).
                              - address (str): The patient's address (can be blank).
                              - emergency_contact_name (str): The name of the emergency contact (max 100 characters).
                              - emergency_contact_phone (str): The phone number of the emergency contact (max 15 characters, e.g., +1234567890).
                              - is_active (bool): Whether the patient is active.
            pk (int): The primary key of the patient to update.

        Returns:
            Response: A JSON response containing the updated serialized patient object on success with status code 200 OK.
                      If the patient is not found, returns status code 404 Not Found.
                      If the input data is invalid (e.g., duplicate medical record number or invalid phone), returns errors with status code 400 Bad Request.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        patient = self.get_object(pk)
        if patient is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a patient by its ID.

        Parameters:
            request (Request): The HTTP request object.
            pk (int): The primary key of the patient to delete.

        Returns:
            Response: A response with status code 204 No Content on successful deletion.
                      If the patient is not found, returns status code 404 Not Found.

        Authentication:
            Requires a valid authentication token in the Authorization header.
        """
        patient = self.get_object(pk)
        if patient is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)