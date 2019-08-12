CREATE OR REPLACE VIEW
"Salmonella_view_apcc" AS
WITH
t2 as (SELECT ap2_0.id ap2_0, ap2_0.st ap2_0_st, ap2_0.dst ap2_0_dst, cc1_2.identifier cc1_2, cc1_2.merge_id_id cc1_2_merge
FROM "Salmonella_cc1_2" cc1_2 RIGHT OUTER JOIN "Salmonella_ap2_0" ap2_0
ON ap2_0.cc1_2_id = cc1_2.identifier)
select mgt.id mgt_id,
t2.ap2_0, t2.ap2_0_st, t2.ap2_0_dst,
t2.cc1_2, t2.cc1_2_merge
from "Salmonella_mgt" as mgt LEFT OUTER JOIN t2
on mgt.ap2_0_id = t2.ap2_0;

grant select on "Salmonella_view_apcc" to mlstWebsite;


-- CREATE OR REPLACE VIEW
-- "Salmonella_view_apcc" AS
-- WITH
-- t2 as (SELECT ap2_0.id ap2_0, ap2_0.st ap2_0_st, ap2_0.dst ap2_0_dst, cc1_2.identifier cc1_2, cc1_2.merge_id_id cc1_2_merge
-- FROM "Salmonella_cc1_2" cc1_2 RIGHT OUTER JOIN "Salmonella_ap2_0" ap2_0
-- ON ap2_0.cc1_2_id = cc1_2.identifier),
-- t3 as (SELECT ap3_0.id ap3_0, ap3_0.st ap3_0_st, ap3_0.dst ap3_0_dst, cc1_3.identifier cc1_3, cc1_3.merge_id_id cc1_3_merge
-- FROM "Salmonella_cc1_3" cc1_3 RIGHT OUTER JOIN "Salmonella_ap3_0" ap3_0
-- ON ap3_0.cc1_3_id = cc1_3.identifier),
-- t4 as (SELECT ap4_0.id ap4_0, ap4_0.st ap4_0_st, ap4_0.dst ap4_0_dst, cc1_4.identifier cc1_4, cc1_4.merge_id_id cc1_4_merge
-- FROM "Salmonella_cc1_4" cc1_4 RIGHT OUTER JOIN "Salmonella_ap4_0" ap4_0
-- ON ap4_0.cc1_4_id = cc1_4.identifier),
-- t5 as (SELECT ap5_0.id ap5_0, ap5_0.st ap5_0_st, ap5_0.dst ap5_0_dst, cc1_5.identifier cc1_5, cc1_5.merge_id_id cc1_5_merge
-- FROM "Salmonella_cc1_5" cc1_5 RIGHT OUTER JOIN "Salmonella_ap5_0" ap5_0
-- ON ap5_0.cc1_5_id = cc1_5.identifier),
-- t6 as (SELECT ap6_0.id ap6_0, ap6_0.st ap6_0_st, ap6_0.dst ap6_0_dst, cc1_6.identifier cc1_6, cc1_6.merge_id_id cc1_6_merge
-- FROM "Salmonella_cc1_6" cc1_6 RIGHT OUTER JOIN "Salmonella_ap6_0" ap6_0
-- ON ap6_0.cc1_6_id = cc1_6.identifier),
-- t7 as (SELECT ap7_0.id ap7_0, ap7_0.st ap7_0_st, ap7_0.dst ap7_0_dst, cc1_7.identifier cc1_7, cc1_7.merge_id_id cc1_7_merge
-- FROM "Salmonella_cc1_7" cc1_7 RIGHT OUTER JOIN "Salmonella_ap7_0" ap7_0
-- ON ap7_0.cc1_7_id = cc1_7.identifier),
-- t8 as (SELECT ap8_0.id ap8_0, ap8_0.st ap8_0_st, ap8_0.dst ap8_0_dst, cc1_8.identifier cc1_8, cc1_8.merge_id_id cc1_8_merge
-- FROM "Salmonella_cc1_8" cc1_8 RIGHT OUTER JOIN "Salmonella_ap8_0" ap8_0
-- ON ap8_0.cc1_8_id = cc1_8.identifier),
-- t9 as (SELECT ap9_0.id ap9_0, ap9_0.st ap9_0_st, ap9_0.dst ap9_0_dst, cc1_9.identifier cc1_9, cc1_9.merge_id_id cc1_9_merge, cc1_9.identifier cc2_1, cc1_9.merge_id_id cc2_1_merge, cc2_2.identifier cc2_2, cc2_2.merge_id_id cc2_2_merge, cc2_3.identifier cc2_3, cc2_3.merge_id_id cc2_3_merge, cc2_4.identifier cc2_4, cc2_4.merge_id_id cc2_4_merge
-- FROM "Salmonella_ap9_0" ap9_0
-- LEFT OUTER JOIN "Salmonella_cc1_9" cc1_9
-- ON ap9_0.cc1_9_id = cc1_9.identifier
-- LEFT OUTER JOIN "Salmonella_cc2_2" cc2_2
-- ON ap9_0.cc2_2_id = cc2_2.identifier
-- LEFT OUTER JOIN "Salmonella_cc2_3" cc2_3
-- ON ap9_0.cc2_3_id = cc2_3.identifier
-- LEFT OUTER JOIN "Salmonella_cc2_4" cc2_4
-- ON ap9_0.cc2_4_id = cc2_4.identifier)
-- select mgt.id mgt_id,
-- t2.ap2_0, t2.ap2_0_st, t2.ap2_0_dst,
-- t3.ap3_0, t3.ap3_0_st, t3.ap3_0_dst,
-- t4.ap4_0, t4.ap4_0_st, t4.ap4_0_dst,
-- t5.ap5_0, t5.ap5_0_st, t5.ap5_0_dst,
-- t6.ap6_0, t6.ap6_0_st, t6.ap6_0_dst,
-- t7.ap7_0, t7.ap7_0_st, t7.ap7_0_dst,
-- t8.ap8_0, t8.ap8_0_st, t8.ap8_0_dst,
-- t9.ap9_0, t9.ap9_0_st, t9.ap9_0_dst,
-- t2.cc1_2, t2.cc1_2_merge,
-- t3.cc1_3, t3.cc1_3_merge,
-- t4.cc1_4, t4.cc1_4_merge,
-- t5.cc1_5, t5.cc1_5_merge,
-- t6.cc1_6, t6.cc1_6_merge,
-- t7.cc1_7, t7.cc1_7_merge,
-- t8.cc1_8, t8.cc1_8_merge,
-- t9.cc1_9, t9.cc1_9_merge,
-- t9.cc2_1, t9.cc2_1_merge,
-- t9.cc2_2, t9.cc2_2_merge,
-- t9.cc2_3, t9.cc2_3_merge,
-- t9.cc2_4, t9.cc2_4_merge
-- from "Salmonella_mgt" as mgt LEFT OUTER JOIN t2
-- on mgt.ap2_0_id = t2.ap2_0
-- LEFT OUTER JOIN t3
-- on mgt.ap3_0_id = t3.ap3_0
-- LEFT OUTER JOIN t4
-- on mgt.ap4_0_id = t4.ap4_0
-- LEFT OUTER JOIN t5
-- on mgt.ap5_0_id = t5.ap5_0
-- LEFT OUTER JOIN t6
-- on mgt.ap6_0_id = t6.ap6_0
-- LEFT OUTER JOIN t7
-- on mgt.ap7_0_id = t7.ap7_0
-- LEFT OUTER JOIN t8
-- on mgt.ap8_0_id = t8.ap8_0
-- LEFT OUTER JOIN t9
-- on mgt.ap9_0_id = t9.ap9_0;
--
-- grant select on "Salmonella_view_apcc" to mlstWebsite;

