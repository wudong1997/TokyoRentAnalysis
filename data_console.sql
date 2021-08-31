create table new_table(
    select Mansion,
           full_address,
           avg(rent + mana) as rent,
           avg(deposit) as disposit,
           avg(gratuity) as gratuity,
           `room-type`,
           avg(area) as area,
           avg(unit_rent) as unit_rent
    from (
        select *,
               concat(Address, Mansion) as full_address,
               ifnull(`management-cost`, 0) as mana,
               rent/area as unit_rent
        from aim_table
        ) as temp
    where  `room-type` = '1K' or `room-type` = '1DK'
    group by Mansion,
             Address,
             `room-type`
    )
