import csv
from app import app, db, Player, Team

player_data = """Set,Player Name,Role,Credit Points,Base Price
Marquee,Virat Kohli,Batter,9.8,2.00 Crore
Marquee,Jasprit Bumrah,Bowler,9.8,2.00 Crore
Marquee,Rishabh Pant,WK/Batter,9.6,2.00 Crore
Marquee,MS Dhoni,WK/Batter,9.8,2.00 Crore
Marquee,Heinrich Klaasen,WK/Batter,9.5,2.00 Crore
Marquee,Rashid Khan,All-Rounder,9.4,2.00 Crore
Marquee,Hardik Pandya,All-Rounder,9.7,2.00 Crore
Marquee,Suryakumar Yadav,Batter,9.4,2.00 Crore
Marquee,Shubman Gill,Batter,8.9,2.00 Crore
Marquee,Yashasvi Jaiswal,Batter,9.5,2.00 Crore
Marquee,Pat Cummins,All-Rounder,9.4,2.00 Crore
Marquee,Nicholas Pooran,WK/Batter,9.5,2.00 Crore
Marquee,Shreyas Iyer,Batter,9.4,2.00 Crore
Marquee,Rohit Sharma,Batter,9.4,2.00 Crore
Marquee,KL Rahul,WK/Batter,9.5,2.00 Crore
Marquee,Travis Head,Batter,9.5,2.00 Crore
Marquee,Mitchell Starc,Bowler,9.3,2.00 Crore
Marquee,Jos Buttler,WK/Batter,9.0,2.00 Crore
Marquee,Kagiso Rabada,Bowler,9.0,2.00 Crore
Marquee,Trent Boult,Bowler,9.0,2.00 Crore
Marquee,Ruturaj Gaikwad,Batter,9.0,2.00 Crore
Capped Batter,Rinku Singh,Batter,8.5,2.00 Crore
Capped Batter,Tilak Varma,Batter,8.5,2.00 Crore
Capped Batter,Sai Sudharsan,Batter,8.5,2.00 Crore
Capped Batter,Rajat Patidar,Batter,8.5,2.00 Crore
Capped Batter,Abhishek Sharma,Batter,8.5,2.00 Crore
Capped Batter,Shivam Dube,Batter,8.5,2.00 Crore
Capped Batter,David Miller,Batter,8.5,2.00 Crore
Capped Batter,Jake Fraser-McGurk,Batter,8.5,2.00 Crore
Capped Batter,Tristan Stubbs,Batter,8.5,2.00 Crore
Capped Batter,Rovman Powell,Batter,8.0,1.5 Crore
Capped Batter,Shimron Hetmyer,Batter,8.0,1.5 Crore
Capped Batter,Tim David,Batter,8.0,1.5 Crore
Capped Batter,Harry Brook,Batter,8.0,1.5 Crore
Capped Batter,Devdutt Padikkal,Batter,7.5,1.5 Crore
Capped Batter,Nitish Rana,Batter,7.5,1.5 Crore
Capped Batter,Kane Williamson,Batter,7.5,1.5 Crore
Capped Batter,Faf du Plessis,Batter,7.5,1.5 Crore
Capped Batter,Jonny Bairstow,Batter,7.5,1.5 Crore
Capped Batter,Jason Roy,Batter,7.5,1.5 Crore
Capped Batter,Prithvi Shaw,Batter,7.0,1.0 Crore
Capped Batter,Mayank Agarwal,Batter,7.0,1.0 Crore
Capped Batter,Manish Pandey,Batter,7.0,1.0 Crore
Capped Batter,Ajinkya Rahane,Batter,7.0,1.0 Crore
Capped Batter,Deepak Hooda,Batter,7.0,1.0 Crore
Capped Batter,Rilee Rossouw,Batter,7.0,1.0 Crore
Capped Batter,Steve Smith,Batter,7.0,1.0 Crore
Capped Batter,David Warner,Batter,7.0,1.0 Crore
Capped Batter,Finn Allen,Batter,7.0,1.0 Crore
Capped Batter,Aiden Markram,Batter,7.0,1.0 Crore
Capped Batter,Will Jacks,Batter,7.0,1.0 Crore
Capped Batter,Rahul Tripathi,Batter,6.5,50 Lakhs
Capped Batter,Ben Duckett,Batter,6.5,50 Lakhs
Capped Batter,Rohan Kunnummal,Batter,6.0,50 Lakhs
Capped Batter,Sherfane Rutherford,Batter,6.0,50 Lakhs
Capped Batter,Donovan Ferreira,Batter,6.0,50 Lakhs
Capped Batter,Matthew Breetzke,Batter,6.0,50 Lakhs
Capped Batter,Ryan Rickelton,Batter,6.0,50 Lakhs
Capped Batter,Martin Guptill,Batter,6.0,50 Lakhs
Capped Batter,Dawid Malan,Batter,6.0,50 Lakhs
Capped Batter,Paul Stirling,Batter,6.0,50 Lakhs
Capped Batter,Brandon King,Batter,6.0,50 Lakhs
Capped Batter,Evin Lewis,Batter,6.0,50 Lakhs
Capped Batter,Najibullah Zadran,Batter,6.0,50 Lakhs
Capped WK,Sanju Samson,WK/Batter,9.0,2.00 Crore
Capped WK,Phil Salt,WK/Batter,8.5,2.00 Crore
Capped WK,Ishan Kishan,WK/Batter,8.5,2.00 Crore
Capped WK,Quinton de Kock,WK/Batter,8.0,1.5 Crore
Capped WK,Devon Conway,WK/Batter,8.0,1.5 Crore
Capped WK,Dhruv Jurel,WK/Batter,8.0,1.5 Crore
Capped WK,Jitesh Sharma,WK/Batter,7.5,1.5 Crore
Capped WK,Rahmanullah Gurbaz,WK/Batter,7.5,1.5 Crore
Capped WK,Matthew Wade,WK/Batter,7.0,1.0 Crore
Capped WK,Josh Inglis,WK/Batter,7.0,1.0 Crore
Capped WK,Alex Carey,WK/Batter,6.5,50 Lakhs
Capped WK,Shai Hope,WK/Batter,6.5,50 Lakhs
Capped WK,Kusal Mendis,WK/Batter,6.5,50 Lakhs
Capped WK,KS Bharat,WK/Batter,6.0,50 Lakhs
Capped WK,Upendra Yadav,WK/Batter,6.0,50 Lakhs
Capped WK,Johnson Charles,WK/Batter,6.0,50 Lakhs
Capped WK,Bhanuka Rajapaksa,WK/Batter,6.0,50 Lakhs
Capped WK,Liton Das,WK/Batter,6.0,50 Lakhs
Capped WK,Tom Banton,WK/Batter,6.0,50 Lakhs
Capped WK,Glenn Phillips,WK/Batter,6.0,50 Lakhs
Capped All-Rounder,Ravindra Jadeja,All-Rounder,9.0,2.00 Crore
Capped All-Rounder,Axar Patel,All-Rounder,9.0,2.00 Crore
Capped All-Rounder,Cameron Green,All-Rounder,9.0,2.00 Crore
Capped All-Rounder,Andre Russell,All-Rounder,9.0,2.00 Crore
Capped All-Rounder,Sunil Narine,All-Rounder,9.0,2.00 Crore
Capped All-Rounder,Sam Curran,All-Rounder,8.5,2.00 Crore
Capped All-Rounder,Marcus Stoinis,All-Rounder,8.5,2.00 Crore
Capped All-Rounder,Ben Stokes,All-Rounder,8.5,2.00 Crore
Capped All-Rounder,Liam Livingstone,All-Rounder,8.5,2.00 Crore
Capped All-Rounder,Glenn Maxwell,All-Rounder,8.5,2.00 Crore
Capped All-Rounder,Rachin Ravindra,All-Rounder,8.5,2.00 Crore
Capped All-Rounder,Nitish Kumar Reddy,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Washington Sundar,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Venkatesh Iyer,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Mitchell Marsh,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Moeen Ali,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Daryl Mitchell,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Will Jacks,All-Rounder,8.0,1.5 Crore
Capped All-Rounder,Azmatullah Omarzai,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Romario Shepherd,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Jason Holder,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Kyle Mayers,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Marco Jansen,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Mitchell Santner,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Krunal Pandya,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Riyan Parag,All-Rounder,7.5,1.5 Crore
Capped All-Rounder,Shahbaz Ahmed,All-Rounder,7.0,1.0 Crore
Capped All-Rounder,Shakib Al Hasan,All-Rounder,7.0,1.0 Crore
Capped All-Rounder,Mohammad Nabi,All-Rounder,7.0,1.0 Crore
Capped All-Rounder,Sikandar Raza,All-Rounder,7.0,1.0 Crore
Capped All-Rounder,Rishi Dhawan,All-Rounder,6.5,50 Lakhs
Capped All-Rounder,Vijay Shankar,All-Rounder,6.5,50 Lakhs
Capped All-Rounder,Chris Woakes,All-Rounder,6.5,50 Lakhs
Capped All-Rounder,David Wiese,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Daniel Sams,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Sean Abbott,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Ashton Agar,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Akeal Hosein,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Fabian Allen,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Odean Smith,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Keemo Paul,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Michael Bracewell,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,James Neesham,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Dasun Shanaka,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Gulbadin Naib,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Karim Janat,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Roelof van der Merwe,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Chris Jordan,All-Rounder,6.0,50 Lakhs
Capped All-Rounder,Tom Curran,All-Rounder,6.0,50 Lakhs
Capped Bowler,Matheesha Pathirana,Bowler,9.0,2.00 Crore
Capped Bowler,Arshdeep Singh,Bowler,9.0,2.00 Crore
Capped Bowler,Mohammed Shami,Bowler,9.0,2.00 Crore
Capped Bowler,Mohammed Siraj,Bowler,9.0,2.00 Crore
Capped Bowler,Kuldeep Yadav,Bowler,9.0,2.00 Crore
Capped Bowler,Yuzvendra Chahal,Bowler,9.0,2.00 Crore
Capped Bowler,Varun Chakaravarthy,Bowler,8.5,2.00 Crore
Capped Bowler,Ravi Bishnoi,Bowler,8.5,2.00 Crore
Capped Bowler,Josh Hazlewood,Bowler,8.5,2.00 Crore
Capped Bowler,Jofra Archer,Bowler,8.5,2.00 Crore
Capped Bowler,Harshit Rana,Bowler,8.5,2.00 Crore
Capped Bowler,Mayank Yadav,Bowler,8.5,2.00 Crore
Capped Bowler,Khaleel Ahmed,Bowler,8.0,1.5 Crore
Capped Bowler,Avesh Khan,Bowler,8.0,1.5 Crore
Capped Bowler,Mukesh Kumar,Bowler,8.0,1.5 Crore
Capped Bowler,T Natarajan,Bowler,8.0,1.5 Crore
Capped Bowler,Deepak Chahar,Bowler,8.0,1.5 Crore
Capped Bowler,Ravichandran Ashwin,Bowler,8.0,1.5 Crore
Capped Bowler,Anrich Nortje,Bowler,8.0,1.5 Crore
Capped Bowler,Gerald Coetzee,Bowler,8.0,1.5 Crore
Capped Bowler,Lockie Ferguson,Bowler,8.0,1.5 Crore
Capped Bowler,Wanindu Hasaranga,Bowler,8.0,1.5 Crore
Capped Bowler,Prasidh Krishna,Bowler,7.5,1.5 Crore
Capped Bowler,Sandeep Sharma,Bowler,7.5,1.5 Crore
Capped Bowler,Mohit Sharma,Bowler,7.5,1.5 Crore
Capped Bowler,Tushar Deshpande,Bowler,7.5,1.5 Crore
Capped Bowler,Navdeep Saini,Bowler,7.0,1.0 Crore
Capped Bowler,Umesh Yadav,Bowler,7.0,1.0 Crore
Capped Bowler,Ishant Sharma,Bowler,7.0,1.0 Crore
Capped Bowler,Bhuvneshwar Kumar,Bowler,7.0,1.0 Crore
Capped Bowler,Rahul Chahar,Bowler,7.0,1.0 Crore
Capped Bowler,Maheesh Theekshana,Bowler,7.0,1.0 Crore
Capped Bowler,Noor Ahmad,Bowler,7.0,1.0 Crore
Capped Bowler,Alzarri Joseph,Bowler,7.0,1.0 Crore
Capped Bowler,Naveen-ul-Haq,Bowler,7.0,1.0 Crore
Capped Bowler,Fazalhaq Farooqi,Bowler,7.0,1.0 Crore
Capped Bowler,Mustafizur Rahman,Bowler,7.0,1.0 Crore
Capped Bowler,Adam Zampa,Bowler,7.0,1.0 Crore
Capped Bowler,Nathan Ellis,Bowler,6.5,50 Lakhs
Capped Bowler,Spencer Johnson,Bowler,6.5,50 Lakhs
Capped Bowler,Jason Behrendorff,Bowler,6.5,50 Lakhs
Capped Bowler,Jhye Richardson,Bowler,6.5,50 Lakhs
Capped Bowler,Reece Topley,Bowler,6.5,50 Lakhs
Capped Bowler,Mark Wood,Bowler,6.5,50 Lakhs
Capped Bowler,Adil Rashid,Bowler,6.5,50 Lakhs
Capped Bowler,Lungi Ngidi,Bowler,6.5,50 Lakhs
Capped Bowler,Nandre Burger,Bowler,6.5,50 Lakhs
Capped Bowler,Matt Henry,Bowler,6.5,50 Lakhs
Capped Bowler,Dushmantha Chameera,Bowler,6.5,50 Lakhs
Capped Bowler,Dilshan Madushanka,Bowler,6.5,50 Lakhs
Capped Bowler,Nuwan Thushara,Bowler,6.5,50 Lakhs
Capped Bowler,Obed McCoy,Bowler,6.0,50 Lakhs
Capped Bowler,Taskin Ahmed,Bowler,6.0,50 Lakhs
Capped Bowler,Shoriful Islam,Bowler,6.0,50 Lakhs
Uncapped Batter,Shashank Singh,Batter,7.5,1.5 Crore
Uncapped Batter,Nehal Wadhera,Batter,7.0,1.0 Crore
Uncapped Batter,Ashutosh Sharma,Batter,7.0,1.0 Crore
Uncapped Batter,Sameer Rizvi,Batter,6.5,50 Lakhs
Uncapped Batter,Angkrish Raghuvanshi,Batter,6.5,50 Lakhs
Uncapped Batter,Abhinav Manohar,Batter,6.5,50 Lakhs
Uncapped Batter,Abdul Samad,Batter,6.5,50 Lakhs
Uncapped Batter,Ayush Badoni,Batter,6.5,50 Lakhs
Uncapped Batter,Prabhsimran Singh,Batter,6.5,50 Lakhs
Uncapped Batter,Harpreet Singh Bhatia,Batter,6.0,50 Lakhs
Uncapped Batter,Atharva Taide,Batter,6.0,50 Lakhs
Uncapped Batter,Yash Dhull,Batter,6.0,50 Lakhs
Uncapped Batter,Priyam Garg,Batter,6.0,50 Lakhs
Uncapped Batter,Virat Singh,Batter,6.0,50 Lakhs
Uncapped Batter,Rahul Deshpande,Batter,5.5,25 Lakhs
Uncapped Batter,Swastik Chikara,Batter,5.5,25 Lakhs
Uncapped Batter,Aryan Juyal,Batter,5.5,25 Lakhs
Uncapped Batter,Shaik Rasheed,Batter,5.5,25 Lakhs
Uncapped Batter,Avanish Rao,Batter,5.5,25 Lakhs
Uncapped Batter,Amandeep Khare,Batter,5.5,25 Lakhs
Uncapped Batter,Rohan Kadam,Batter,5.5,25 Lakhs
Uncapped Batter,Sachin Baby,Batter,5.5,25 Lakhs
Uncapped Batter,Anmolpreet Singh,Batter,5.5,25 Lakhs
Uncapped Batter,Suyash Prabhudessai,Batter,5.5,25 Lakhs
Uncapped Batter,Saurabh Tiwary,Batter,5.0,25 Lakhs
Uncapped Batter,Himmat Singh,Batter,5.0,25 Lakhs
Uncapped Batter,Rajat Bhatia,Batter,5.0,25 Lakhs
Uncapped Batter,Nishant Sindhu,Batter,5.0,25 Lakhs
Uncapped Batter,Bipin Saurabh,Batter,5.0,25 Lakhs
Uncapped Batter,Kumar Suraj,Batter,5.0,25 Lakhs
Uncapped Batter,Priyansh Arya,Batter,5.0,25 Lakhs
Uncapped Batter,Ayush Mhatre,Batter,5.0,25 Lakhs
Uncapped Batter,Musheer Khan,Batter,5.0,25 Lakhs
Uncapped Batter,Ankit Kumar,Batter,5.0,25 Lakhs
Uncapped Batter,Samarth Vyas,Batter,5.0,25 Lakhs
Uncapped WK,Robin Minz,WK/Batter,6.5,50 Lakhs
Uncapped WK,Kumar Kushagra,WK/Batter,6.0,50 Lakhs
Uncapped WK,B.R. Sharath,WK/Batter,5.5,25 Lakhs
Uncapped WK,Ricky Bhui,WK/Batter,5.5,25 Lakhs
Uncapped WK,Luvnith Sisodia,WK/Batter,5.5,25 Lakhs
Uncapped WK,Vishnu Vinod,WK/Batter,5.5,25 Lakhs
Uncapped WK,Narayan Jagadeesan,WK/Batter,5.5,25 Lakhs
Uncapped WK,Agnivesh Ayachi,WK/Batter,5.0,25 Lakhs
Uncapped WK,Pradosh Ranjan Paul,WK/Batter,5.0,25 Lakhs
Uncapped WK,Uranoor Singh,WK/Batter,5.0,25 Lakhs
Uncapped WK,Sumit Kumar,WK/Batter,5.0,25 Lakhs
Uncapped WK,Kedar Jadhav,WK/Batter,5.0,25 Lakhs
Uncapped WK,Sheldon Jackson,WK/Batter,5.0,25 Lakhs
Uncapped WK,Shreevats Goswami,WK/Batter,5.0,25 Lakhs
Uncapped WK,Smit Patel,WK/Batter,5.0,25 Lakhs
Uncapped All-Rounder,Ramandeep Singh,All-Rounder,7.0,1.0 Crore
Uncapped All-Rounder,Naman Dhir,All-Rounder,6.5,50 Lakhs
Uncapped All-Rounder,Shahrukh Khan,All-Rounder,6.5,50 Lakhs
Uncapped All-Rounder,Mahipal Lomror,All-Rounder,6.5,50 Lakhs
Uncapped All-Rounder,Harpreet Brar,All-Rounder,6.5,50 Lakhs
Uncapped All-Rounder,Prerak Mankad,All-Rounder,6.0,50 Lakhs
Uncapped All-Rounder,Sanvir Singh,All-Rounder,6.0,50 Lakhs
Uncapped All-Rounder,Vivrant Sharma,All-Rounder,6.0,50 Lakhs
Uncapped All-Rounder,Raj Bawa,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Manoj Bhandage,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Shivalik Sharma,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Praveen Dubey,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Lalit Yadav,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Arshin Kulkarni,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Hrithik Shokeen,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Arshad Khan,All-Rounder,5.5,25 Lakhs
Uncapped All-Rounder,Utkarsh Singh,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Jalaj Saxena,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Swapnil Singh,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Gaurav Yadav,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Ninad Rathva,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Pratham Singh,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Darshan Nalkande,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Vipul Krishna,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Ravi Teja,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Sanjay Yadav,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Shubham Dubey,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Pankaj Yadav,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Ayush Pandey,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Kritik Yadav,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Rishi Singh,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Aman Khan,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Akash Singh,All-Rounder,5.0,25 Lakhs
Uncapped All-Rounder,Yash Rathod,All-Rounder,5.0,25 Lakhs
Uncapped Bowler,Anshul Kamboj,Bowler,7.5,1.5 Crore
Uncapped Bowler,Yash Dayal,Bowler,7.5,1.5 Crore
Uncapped Bowler,Rasikh Salam,Bowler,7.0,1.0 Crore
Uncapped Bowler,Vidwath Kaverappa,Bowler,6.5,50 Lakhs
Uncapped Bowler,Vyshak Vijaykumar,Bowler,6.5,50 Lakhs
Uncapped Bowler,Mohsin Khan,Bowler,6.5,50 Lakhs
Uncapped Bowler,Kartik Tyagi,Bowler,6.5,50 Lakhs
Uncapped Bowler,Sushant Mishra,Bowler,6.0,50 Lakhs
Uncapped Bowler,Kamlesh Nagarkoti,Bowler,6.0,50 Lakhs
Uncapped Bowler,Shivam Mavi,Bowler,6.0,50 Lakhs
Uncapped Bowler,Manav Suthar,Bowler,6.0,50 Lakhs
Uncapped Bowler,R Sai Kishore,Bowler,6.0,50 Lakhs
Uncapped Bowler,M Siddharth,Bowler,6.0,50 Lakhs
Uncapped Bowler,Suyash Sharma,Bowler,6.0,50 Lakhs
Uncapped Bowler,Akash Madhwal,Bowler,6.0,50 Lakhs
Uncapped Bowler,Kumar Kartikeya,Bowler,5.5,25 Lakhs
Uncapped Bowler,Gurnoor Brar,Bowler,5.5,25 Lakhs
Uncapped Bowler,Kuldip Yadav,Bowler,5.5,25 Lakhs
Uncapped Bowler,Yudhvir Singh,Bowler,5.5,25 Lakhs
Uncapped Bowler,Prashant Solanki,Bowler,5.5,25 Lakhs
Uncapped Bowler,Simarjeet Singh,Bowler,5.5,25 Lakhs
Uncapped Bowler,Rajvardhan Hangargekar,Bowler,5.5,25 Lakhs
Uncapped Bowler,Ishan Porel,Bowler,5.5,25 Lakhs
Uncapped Bowler,Sandeep Warrier,Bowler,5.5,25 Lakhs
Uncapped Bowler,Mayank Markande,Bowler,5.5,25 Lakhs
Uncapped Bowler,Shreyas Gopal,Bowler,5.5,25 Lakhs
Uncapped Bowler,Karn Sharma,Bowler,5.0,25 Lakhs
Uncapped Bowler,Piyush Chawla,Bowler,5.0,25 Lakhs
Uncapped Bowler,Amit Mishra,Bowler,5.0,25 Lakhs
Uncapped Bowler,Murugan Ashwin,Bowler,5.0,25 Lakhs
Uncapped Bowler,KC Cariappa,Bowler,5.0,25 Lakhs
Uncapped Bowler,Venkatesh M,Bowler,5.0,25 Lakhs
Uncapped Bowler,Vasuki Koushik,Bowler,5.0,25 Lakhs
Uncapped Bowler,Prince Choudhary,Bowler,5.0,25 Lakhs
Uncapped Bowler,Ranjan Paul,Bowler,5.0,25 Lakhs
"""

def seed_db():
    with app.app_context():
        # Clean current DB
        db.drop_all()
        db.create_all()

        # Seed Teams
        print("Seeding teams...")
        teams = [
            "Chennai Super Kings (CSK)",
            "Mumbai Indians (MI)",
            "Royal Challengers Bengaluru (RCB)",
            "Kolkata Knight Riders (KKR)",
            "Sunrisers Hyderabad (SRH)",
            "Delhi Capitals (DC)",
            "Rajasthan Royals (RR)",
            "Punjab Kings (PBKS)"
        ]
        
        for t_name in teams:
            db.session.add(Team(name=t_name))
        
        # Seed players
        import io
        reader = csv.DictReader(io.StringIO(player_data))
        for row in reader:
            set_name = row['Set']
            name = row['Player Name']
            role = row['Role']
            credits_val = row['Credit Points']
            base_price = row['Base Price']

            if role == "Batter":
                role = "Batsman" # standardizing
            elif role == "WK/Batter":
                role = "Wicketkeeper"
            elif role == "All-Rounder":
                role = "Allrounder"
            
            p = Player(name=name, role=role, set_name=set_name, base_price=base_price, credits=float(credits_val))
            db.session.add(p)
        
        db.session.commit()
        print("Database newly seeded successfully with provided list!")

if __name__ == "__main__":
    seed_db()
