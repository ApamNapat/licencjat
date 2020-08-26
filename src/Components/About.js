import React from 'react';

const About = () => {
    return (
        <div>
            <h3>About</h3>
            <p>In this game you are a CS student at the University of Wrocław. Go to classes, learn, party, and some day
                you just might finish the 6th semester and get your Bachelor's.</p>
            <p>Every semester lasts 14 "days". Through <b>Set Timetable</b> you can set your actions for up to 12
                upcoming hours and then monitor your progress at <b>Your Timetable</b>.</p>
            <p>After 14 days the semester ends, you will be able to take an exam for every class which you have attended
                at least 10 times. Your scores depend on the abilities you earned and the skills that the class
                improves. Keep in mind that the classes from higher semesters are harder, and the ones from
                lower semesters won't teach you as much. If you get enough ECTS points you will move into a next
                semester, otherwise you will stay at the current semester, but once you fail a second time, you're
                out!</p>
            <p>Aside from learning and attending classes you also have to take care of yourself! Your mood influences
                your performance at most actions. And while you can keep on going even at low energy
                once it drops below 10 you won't be able to go on.
            </p>
            <p>Eating, drinking and a roof over your head are not free, so remember to work, at the end of each day you
                will be charged for all that and if you can't afford it - the stress will lower your Energy and Mood</p>
            <p>Attending classes also gives you a chance to learn new abilities, which you can see at <b>Abilities</b>,
                those are nice to collect and, more importantly, are very important once it comes to passing the exams.
            </p>
            <p>And if you're every wondering what exactly has been happening after each of your actions - check out
                the <b>Messages</b> tab</p>
        </div>
    );
}

export default About;