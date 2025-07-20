
import random
import string

def random_id(prefix):
   number = random.randint(100,999)
   return f"{prefix}{number}"

#BASIC CLASS

class Person:
   def __init__(self,name,age,gender):
      self.name= name
      self.age= age
      self.gender= gender
 
   def display_data(self):
        print(f"Name:{self.name.capitalize()}")
        print(f"Age:{self.age}")
        print(f"Gender:{self.gender.capitalize()}")

#PATIENT CLASS
class Patient(Person):

   def __init__(self, name, age, gender):
      super().__init__(name, age, gender)
      self.patient_id= random_id("P")
      self.appointment_list =[]

   def  book_appointment(self, appointment):
        self.appointment_list.append(appointment)

   def view_profile(self):
      self.display_data()
      print(f"Patient ID:{self.patient_id}")

# DOCTOR CLASS

class Doctor(Person):  

   def __init__(self, name, age, gender, specialty, schedule):
      super().__init__(name, age, gender)
      self.doctor_id = random_id("D")
      self.specialty = specialty
      self.schedule = schedule

   def is_available(self, date, time):
      print(f"\n==========Appointment=========")
      if (date,time) in self.schedule:
         print (f"Dr. {self.name} is unavailable on {date} at {time}.")
         return False
      return True
   

   def view_schedule(self):
      print(f"\nSchedule for Dr. {self.name}:")
      if self.schedule == []:
         print("No appointment yet.")
      else:
         for date_time in self.schedule:
            print(f"Appointment on {date_time[0]} at {date_time[1]}")   

   def view_profile(self):
      self.display_data()
      print(f"Doctor ID : {self.doctor_id}") 
      print(f"Specialty: {self.specialty}")  
      print(f"Schedule: {self.schedule}")

#APPOINTMENT CLASS
class Appointment:
   

   def __init__(self, patient, doctor, date, time):
      self.appointment_id = random_id("A")
      self.patient = patient
      self.doctor = doctor
      self.date = date
      self.time = time
      self.status = "Confirmed"
      

   def confirm(self):
      print(f"\nAppointment {self.appointment_id} is confirmed.")   

   def cancel(self):
      self.status = "Cancelled"
      print(f"\nAppointment {self.appointment_id} is cancelled.")
   
   def display(self):
      print (f'\n-------------------------------------------------------------')
      print(f"Appointment ID: {self.appointment_id}")
      print(f"Patient: {self.patient.name} (ID: {self.patient.patient_id})")
      print(f"Doctor: {self.doctor.name} (ID: {self.doctor.doctor_id})")
      print(f"Date: {self.date}")
      print(f"Time: {self.time}")
      print(f"Status: {self.status}")
      print (f'\n-------------------------------------------------------------')
     

#HOSPITAL SYSTEM CLASS
class HospitalSystem:
   def __init__(self):
      self.patients = {}
      self.doctors = {}
      self.appointments = {}
   
   # Add a new patient
   def add_patient(self, name, age, gender):
            
      try:
         age = int(age)
         if age <= 0:
            raise ValueError
      except ValueError:
               print("Invalid age. Please enter a number above 0.") 
            
      
      
      gender = gender.strip().lower().capitalize()
      if gender not in ['Male', 'Female']:
         print("Invalid gender. Please use 'Male' or 'Female'")
         return  

      patient = Patient(name, age, gender)
      self.patients[patient.patient_id] = patient  
      print(f"------------------------------------------")   
      print(f"\nPatient {patient.name.capitalize()} has been added with ID:{patient.patient_id}")

   
    
   #Add a new doctor
   def add_doctor(self,name,age,gender,specialty,schedule):
      try:

         age = int(age)
         if age <= 0:
            raise ValueError
      except ValueError:
        print("Invalid age. Please enter a number above 0.") 
        return
      
      gender = gender.strip().lower().capitalize()
      if gender not in ['Male', 'Female']:
         print("Invalid gender. Please use 'Male' or 'Female'")
         return  
     
  
      doctor = Doctor(name,age,gender,specialty,schedule)
      self.doctors[doctor.doctor_id] = doctor
      print(f"Doctor {doctor.name.capitalize()} has been added with ID:{doctor.doctor_id}.")

   def book_appointment(self, patient_id, doctor_id, date, time):
         patient = self.patients.get(patient_id)
         if not patient:
            print("Patient ID not found. Please try again.")
            return
   
         doctor = self.doctors.get(doctor_id)
         if not doctor:
            print("Doctor ID not found. Please try again.")
            return
   
         if not doctor.is_available (date,time):
            print("Doctor is not available at this time.")
            return 
         
         for appt in patient.appointment_list: 
            if appt.doctor == doctor and appt.date == date and appt.time == time:
               print ("Appointment already exist.")
               return
   

         appointment= Appointment(patient, doctor, date, time) 
         self.appointments[appointment.appointment_id] = appointment
         patient.book_appointment(appointment)
         doctor.schedule.append((date,time))
         appointment.confirm()
         print("Appointment has been booked successfully. ID:", appointment.appointment_id)
         print(f"\n===================================")

   def cancel_appointment(self, appointment_id):
      appointment = self.appointments.get(appointment_id)
      if appointment and appointment.status == "Confirmed":
         appointment.cancel()  
         try:
            appointment.doctor.schedule.remove((appointment.date, appointment.time))
         except ValueError:
            pass
      else:
         print("Appointment ID not found or cancelled.")   


   #GENERATE BILL
   def generate_bill(self, appointment_id):
      appointment = self.appointments.get(appointment_id)
      if not appointment or appointment.status != "Confirmed":
            print ("Appointment is not valid or already cancelled.")
            return
      
      consultation_fee = 3000

      print("\n==========Better Health Hospital Bill Receipt========== ")
      print("           Manchester Avenue, May Pen,Clarendon ")
      print("                    Tel: 876-224-7838")
      print("=======================================================")
      print(f"Patient: {appointment.patient.name} ") 
      print(f"Doctor: {appointment.doctor.name} ({appointment.doctor.specialty})")
      print(f"Date: {appointment.date} at {appointment.time}")
      print("------------------------------------------------------")
      print(f"Consultation Fee: JMD ${consultation_fee}")
      try: 

         test_fee = float(input("Enter test fee (JMD):$ "))
         medication_fee = float(input("Enter medication fee (JMD):$ "))
         
         if test_fee <0 or medication_fee < 0:
            raise ValueError
      except ValueError:
         print('Invalid amount. Fees must be number greater than 0')
         return
      
      total = consultation_fee + test_fee + medication_fee

      print("-----------------------------------------------------")
      print(f"Total Amount Due: JMD ${total}")
      print("=====================================================")

def main():
      system = HospitalSystem()

      while True:     
         print("\n==========Better Health Hospital==========")
         print("==========================================")
         print("Please choose an option.\n")
         print("1. Add Patient")
         print("2. Add Doctor")
         print("3. Book Appointment")
         print("4. Cancel Appointment")
         print("5. Generate Bill")
         print("6. View Patient Profile") 
         print("7. View Doctor Profile")
         print("8. Exit")
         print("==========================================\n")
      
         choice = input(f"Enter your choice (1-8): ")
      
        #Add Patient
         if choice == "1":
            name = input("Enter patient name: ")
            age = input("Enter patient age: ")
            gender = input("Enter patient gender (male/female): ")
            system.add_patient(name,age,gender)

         #Add Doctor 
         elif choice == "2":   
            name = input("Enter doctor's name: ")
            age = input("Enter doctor's age: ")
            gender = input("Enter doctor's gender: ")
            specialty = input("Enter doctor's specialty: ")
            schedule  = []
            system.add_doctor(name,age,gender,specialty,schedule)
         
         #Book Appointment
         elif choice == "3":   
            PtId = input("Enter Patient ID: ")
            DrId = input("Enter Doctor's ID: ")
            date = input("Enter Date (mm-dd-yyyy): ")
            time = input("Enter time (HH:MM)")
            system.book_appointment(PtId, DrId, date, time)   
         
         #Cancel Appointment
         elif choice == "4":   
            AptId = input("Enter appointment ID: ")
            system.cancel_appointment(AptId)   

         #Generate Bill
         elif choice == "5":
            AptId = input("Enter Appointment ID: ")
            system.generate_bill(AptId)

         #View Patient Profile
         elif choice == "6":
            PtId = input(f"\nEnter Patient ID to view profile: ")
            patient = system.patients.get(PtId)
            if patient: 
               patient.view_profile()
            else:
               print("Patient ID was not found.")   

         #View Doctor Profile
         elif choice =="7":
            DrId = input("Enter doctor ID to view schedule: ")
            doctor =  system.doctors.get(DrId)
            if doctor:
               doctor.view_schedule()
            else:
               print("Doctor's ID was not found.")  

         #Exit
         elif choice == "8" :
            print("Thank you for using Better Health Hospital System. Goodbye!")     

            break
         else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
   main()            


               
        
         