-- 1. What is the top 5 major purpose of taking  loan ?

select loan_purpose, count(loan_id) as total_loans
from loan_applications
group by loan_purpose
order by total_loans DESC limit 5;
--INSIGHTS==>major purpose is home immprovement


-- 2. Who are the borrower who take loan of more than avg loan_amount?Do borrowers taking above-average loans default more often?
with above_avg_loan_taker as (select loan_id, borrower_id, loan_amount,defaulted 
from loan_applications
where loan_amount > (SELECT avg(loan_amount) from loan_applications))

select count(loan_id) from above_avg_loan_taker where defaulted=1;
 
--INSIGHTS==>69 out of 273 person taking above average loan  have defaulted.


-- 3. is there any borrower whose income is more than avg income but still defaulted?
select b.borrower_id, b.annual_income, l.dti_ratio,l.defaulted
from borrower_profiles b 
join loan_applications l 
on b.borrower_id=l.borrower_id
WHERE annual_income > (SELECT avg(annual_income) from borrower_profiles) 
AND
defaulted=1;
-- INSIGHTS==>there are 52 borrowers are like that having more than avg_income but still defaulted. This gives me idea of question 4 as if person is defaulting with high income, then it might because they have high debt also, making it's dti_ratio high.


-- 4. What are the dti_ratio of borrower's, having higher income than avg_income , but defaulted?
with high_income_defaulted as (
select b.borrower_id, b.annual_income, l.dti_ratio,l.defaulted
from borrower_profiles b 
join loan_applications l 
on b.borrower_id=l.borrower_id
WHERE annual_income > (SELECT avg(annual_income) from borrower_profiles) 
AND
defaulted=1)

select borrower_id, dti_ratio
from high_income_defaulted
where dti_ratio > 30.0;
--INSIGHTS==> there are 52 borrowers have defaulted despite having high income and the reason is that they have dti_ratio is high, means having high debt along with high income. 41 out of 52 borrower's having more more than 30 dti_ratio.


--5.. What are the number of default loan in each state?
select b.state, count(l.loan_status) as default_loans
from borrower_profiles b 
join loan_applications l 
on b.borrower_id=l.borrower_id
where loan_status='Default'
GROUP by b.state;
-- INSIGHTS==> MO has high number of default as compared to other states, i.e 13


--6 Find out  the person having safe dti_ratio (less than 30), safe credit_score(>=750) and having income more than avg income and out of this safe borrowers how many have still defaulted?
with safe_borrower as (select b.borrower_id, b.annual_income, b.credit_score, l.dti_ratio, l.loan_status 
from borrower_profiles b
join loan_applications l 
on b.borrower_id=l.borrower_id
where b.annual_income > (select avg(b2.annual_income) from borrower_profiles b2)
AND
l.dti_ratio<30.0
AND 
b.credit_score >=750)

select * from safe_borrower
where loan_status='Default';
-- INSIGHT==> This gives me the most important metrics for loan approval will be dti_ratio, credit_score, and annual_income, as we have found only three person in the safe borrowers are defaulted rest is paid off their loan.so I think choosing dti_ratio<30,credit_score>=750 and income>64471.484 (it is the avg_anuual income) for loan approval reduces the chance of default.


--7. I want to know how much defaulted ,non-defaulted loans and default_percentage in each education level.
select b.education_level,
count(l.loan_status) as total_loans,
sum(case when l.loan_status='Default' then 1 else 0 end) as defaulted_loans,
sum(case when l.loan_status != 'Default' then 1 else 0 end) as non_defaulted_loans,
(sum(case when l.loan_status='Default' then 1.0 else 0.0 end)/count(l.loan_status))*100 as default_pct
from borrower_profiles b
join loan_applications l
on b.borrower_id=l.borrower_id
group by b.education_level;
-- INSIGHT==> large number of loans are taken by bachelor, but the percentage of high default is in doctorate.


--8. default and non-default loans in each home_ownership
select b.home_ownership,
count(l.loan_status) as total_loans,
sum(case when l.loan_status='Default' then 1 else 0 end) as default_loans,
sum(case WHEN l.loan_status !='Default' then 1 else 0 end) as non_default_loans,
(sum(case when l.loan_status='Default' then 1.0 else 0.0 end)/count(l.loan_status))* 100 as default_pct
from borrower_profiles b
join loan_applications l
on b.borrower_id=l.borrower_id
group by b.home_ownership;
--INSIGHT==> large number of people have mortgage their houses(262) but the default percenatage is high with person living on rent.


--9 Which loan purpose has the highest default rate?
select loan_purpose,
(sum(case when loan_status='Default' then 1.0 else 0.0 end)/count(loan_status))* 100 as default_rate
from loan_applications
group by loan_purpose;
--INSIGHT==> Wedding has highest default rate

--10. Which age group defaults the most?
select 
    case
        when b.age between 21 and 30 then '21-30'
        when b.age between 31 and 40 then '31-40'
        when b.age between 41 and 50 then '41-50'
        when b.age between 51 and 60 then '51-60'
        when b.age between 61 and 70 then '61-70'
    end as 'age_group',

count(*) as total_loans,

sum(case when l.loan_status='Default' then 1 else 0 end) as defaulted_loans,

(sum(case when l.loan_status='Default' then 1.0 else 0.0 end)/count(*)) * 100 as default_rate

from borrower_profiles b 
join loan_applications l 
on b.borrower_id=l.borrower_id
GROUP by age_group
order by default_rate desc;
