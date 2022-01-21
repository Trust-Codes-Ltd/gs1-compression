"""tableF indicates the expected format
 for the value of each application identifier."""
TABLE_F = {"00": [{"E": "N", "L": "18"}], "01": [{"E": "N", "L": "14"}],
           "02": [{"E": "N", "L": "14"}], "10": [{"E": "X", "M": "20"}],
           "11": [{"E": "N", "L": "6"}], "12": [{"E": "N", "L": "6"}],
           "13": [{"E": "N", "L": "6"}], "15": [{"E": "N", "L": "6"}],
           "16": [{"E": "N", "L": "6"}], "17": [{"E": "N", "L": "6"}],
           "20": [{"E": "N", "L": "2"}], "21": [{"E": "X", "M": "20"}],
           "22": [{"E": "X", "M": "20"}], "240": [{"E": "X", "M": "30"}],
           "241": [{"E": "X", "M": "30"}], "242": [{"E": "N", "M": "6"}],
           "243": [{"E": "X", "M": "20"}], "250": [{"E": "X", "M": "30"}],
           "251": [{"E": "X", "M": "30"}],
           "253": [{"E": "N", "L": "13"}, {"E": "X", "M": "17"}],
           "254": [{"E": "X", "M": "20"}],
           "255": [{"E": "N", "L": "13"}, {"E": "N", "M": "12"}],
           "30": [{"E": "N", "M": "8"}], "3100": [{"E": "N", "L": "6"}],
           "3101": [{"E": "N", "L": "6"}], "3102": [{"E": "N", "L": "6"}],
           "3103": [{"E": "N", "L": "6"}], "3104": [{"E": "N", "L": "6"}],
           "3105": [{"E": "N", "L": "6"}], "3110": [{"E": "N", "L": "6"}],
           "3111": [{"E": "N", "L": "6"}], "3112": [{"E": "N", "L": "6"}],
           "3113": [{"E": "N", "L": "6"}], "3114": [{"E": "N", "L": "6"}],
           "3115": [{"E": "N", "L": "6"}], "3120": [{"E": "N", "L": "6"}],
           "3121": [{"E": "N", "L": "6"}], "3122": [{"E": "N", "L": "6"}],
           "3123": [{"E": "N", "L": "6"}], "3124": [{"E": "N", "L": "6"}],
           "3125": [{"E": "N", "L": "6"}], "3130": [{"E": "N", "L": "6"}],
           "3131": [{"E": "N", "L": "6"}], "3132": [{"E": "N", "L": "6"}],
           "3133": [{"E": "N", "L": "6"}], "3134": [{"E": "N", "L": "6"}],
           "3135": [{"E": "N", "L": "6"}], "3140": [{"E": "N", "L": "6"}],
           "3141": [{"E": "N", "L": "6"}], "3142": [{"E": "N", "L": "6"}],
           "3143": [{"E": "N", "L": "6"}], "3144": [{"E": "N", "L": "6"}],
           "3145": [{"E": "N", "L": "6"}], "3150": [{"E": "N", "L": "6"}],
           "3151": [{"E": "N", "L": "6"}], "3152": [{"E": "N", "L": "6"}],
           "3153": [{"E": "N", "L": "6"}], "3154": [{"E": "N", "L": "6"}],
           "3155": [{"E": "N", "L": "6"}], "3160": [{"E": "N", "L": "6"}],
           "3161": [{"E": "N", "L": "6"}], "3162": [{"E": "N", "L": "6"}],
           "3163": [{"E": "N", "L": "6"}], "3164": [{"E": "N", "L": "6"}],
           "3165": [{"E": "N", "L": "6"}], "3200": [{"E": "N", "L": "6"}],
           "3201": [{"E": "N", "L": "6"}], "3202": [{"E": "N", "L": "6"}],
           "3203": [{"E": "N", "L": "6"}], "3204": [{"E": "N", "L": "6"}],
           "3205": [{"E": "N", "L": "6"}], "3210": [{"E": "N", "L": "6"}],
           "3211": [{"E": "N", "L": "6"}], "3212": [{"E": "N", "L": "6"}],
           "3213": [{"E": "N", "L": "6"}], "3214": [{"E": "N", "L": "6"}],
           "3215": [{"E": "N", "L": "6"}], "3220": [{"E": "N", "L": "6"}],
           "3221": [{"E": "N", "L": "6"}], "3222": [{"E": "N", "L": "6"}],
           "3223": [{"E": "N", "L": "6"}], "3224": [{"E": "N", "L": "6"}],
           "3225": [{"E": "N", "L": "6"}], "3230": [{"E": "N", "L": "6"}],
           "3231": [{"E": "N", "L": "6"}], "3232": [{"E": "N", "L": "6"}],
           "3233": [{"E": "N", "L": "6"}], "3234": [{"E": "N", "L": "6"}],
           "3235": [{"E": "N", "L": "6"}], "3240": [{"E": "N", "L": "6"}],
           "3241": [{"E": "N", "L": "6"}], "3242": [{"E": "N", "L": "6"}],
           "3243": [{"E": "N", "L": "6"}], "3244": [{"E": "N", "L": "6"}],
           "3245": [{"E": "N", "L": "6"}], "3250": [{"E": "N", "L": "6"}],
           "3251": [{"E": "N", "L": "6"}], "3252": [{"E": "N", "L": "6"}],
           "3253": [{"E": "N", "L": "6"}], "3254": [{"E": "N", "L": "6"}],
           "3255": [{"E": "N", "L": "6"}], "3260": [{"E": "N", "L": "6"}],
           "3261": [{"E": "N", "L": "6"}], "3262": [{"E": "N", "L": "6"}],
           "3263": [{"E": "N", "L": "6"}], "3264": [{"E": "N", "L": "6"}],
           "3265": [{"E": "N", "L": "6"}], "3270": [{"E": "N", "L": "6"}],
           "3271": [{"E": "N", "L": "6"}], "3272": [{"E": "N", "L": "6"}],
           "3273": [{"E": "N", "L": "6"}], "3274": [{"E": "N", "L": "6"}],
           "3275": [{"E": "N", "L": "6"}], "3280": [{"E": "N", "L": "6"}],
           "3281": [{"E": "N", "L": "6"}], "3282": [{"E": "N", "L": "6"}],
           "3283": [{"E": "N", "L": "6"}], "3284": [{"E": "N", "L": "6"}],
           "3285": [{"E": "N", "L": "6"}], "3290": [{"E": "N", "L": "6"}],
           "3291": [{"E": "N", "L": "6"}], "3292": [{"E": "N", "L": "6"}],
           "3293": [{"E": "N", "L": "6"}], "3294": [{"E": "N", "L": "6"}],
           "3295": [{"E": "N", "L": "6"}], "3300": [{"E": "N", "L": "6"}],
           "3301": [{"E": "N", "L": "6"}], "3302": [{"E": "N", "L": "6"}],
           "3303": [{"E": "N", "L": "6"}], "3304": [{"E": "N", "L": "6"}],
           "3305": [{"E": "N", "L": "6"}], "3310": [{"E": "N", "L": "6"}],
           "3311": [{"E": "N", "L": "6"}], "3312": [{"E": "N", "L": "6"}],
           "3313": [{"E": "N", "L": "6"}], "3314": [{"E": "N", "L": "6"}],
           "3315": [{"E": "N", "L": "6"}], "3320": [{"E": "N", "L": "6"}],
           "3321": [{"E": "N", "L": "6"}], "3322": [{"E": "N", "L": "6"}],
           "3323": [{"E": "N", "L": "6"}], "3324": [{"E": "N", "L": "6"}],
           "3325": [{"E": "N", "L": "6"}], "3330": [{"E": "N", "L": "6"}],
           "3331": [{"E": "N", "L": "6"}], "3332": [{"E": "N", "L": "6"}],
           "3333": [{"E": "N", "L": "6"}], "3334": [{"E": "N", "L": "6"}],
           "3335": [{"E": "N", "L": "6"}], "3340": [{"E": "N", "L": "6"}],
           "3341": [{"E": "N", "L": "6"}], "3342": [{"E": "N", "L": "6"}],
           "3343": [{"E": "N", "L": "6"}], "3344": [{"E": "N", "L": "6"}],
           "3345": [{"E": "N", "L": "6"}], "3350": [{"E": "N", "L": "6"}],
           "3351": [{"E": "N", "L": "6"}], "3352": [{"E": "N", "L": "6"}],
           "3353": [{"E": "N", "L": "6"}], "3354": [{"E": "N", "L": "6"}],
           "3355": [{"E": "N", "L": "6"}], "3360": [{"E": "N", "L": "6"}],
           "3361": [{"E": "N", "L": "6"}], "3362": [{"E": "N", "L": "6"}],
           "3363": [{"E": "N", "L": "6"}], "3364": [{"E": "N", "L": "6"}],
           "3365": [{"E": "N", "L": "6"}], "3370": [{"E": "N", "L": "6"}],
           "3371": [{"E": "N", "L": "6"}], "3372": [{"E": "N", "L": "6"}],
           "3373": [{"E": "N", "L": "6"}], "3374": [{"E": "N", "L": "6"}],
           "3375": [{"E": "N", "L": "6"}], "3400": [{"E": "N", "L": "6"}],
           "3401": [{"E": "N", "L": "6"}], "3402": [{"E": "N", "L": "6"}],
           "3403": [{"E": "N", "L": "6"}], "3404": [{"E": "N", "L": "6"}],
           "3405": [{"E": "N", "L": "6"}], "3410": [{"E": "N", "L": "6"}],
           "3411": [{"E": "N", "L": "6"}], "3412": [{"E": "N", "L": "6"}],
           "3413": [{"E": "N", "L": "6"}], "3414": [{"E": "N", "L": "6"}],
           "3415": [{"E": "N", "L": "6"}], "3420": [{"E": "N", "L": "6"}],
           "3421": [{"E": "N", "L": "6"}], "3422": [{"E": "N", "L": "6"}],
           "3423": [{"E": "N", "L": "6"}], "3424": [{"E": "N", "L": "6"}],
           "3425": [{"E": "N", "L": "6"}], "3430": [{"E": "N", "L": "6"}],
           "3431": [{"E": "N", "L": "6"}], "3432": [{"E": "N", "L": "6"}],
           "3433": [{"E": "N", "L": "6"}], "3434": [{"E": "N", "L": "6"}],
           "3435": [{"E": "N", "L": "6"}], "3440": [{"E": "N", "L": "6"}],
           "3441": [{"E": "N", "L": "6"}], "3442": [{"E": "N", "L": "6"}],
           "3443": [{"E": "N", "L": "6"}], "3444": [{"E": "N", "L": "6"}],
           "3445": [{"E": "N", "L": "6"}], "3450": [{"E": "N", "L": "6"}],
           "3451": [{"E": "N", "L": "6"}], "3452": [{"E": "N", "L": "6"}],
           "3453": [{"E": "N", "L": "6"}], "3454": [{"E": "N", "L": "6"}],
           "3455": [{"E": "N", "L": "6"}], "3460": [{"E": "N", "L": "6"}],
           "3461": [{"E": "N", "L": "6"}], "3462": [{"E": "N", "L": "6"}],
           "3463": [{"E": "N", "L": "6"}], "3464": [{"E": "N", "L": "6"}],
           "3465": [{"E": "N", "L": "6"}], "3470": [{"E": "N", "L": "6"}],
           "3471": [{"E": "N", "L": "6"}], "3472": [{"E": "N", "L": "6"}],
           "3473": [{"E": "N", "L": "6"}], "3474": [{"E": "N", "L": "6"}],
           "3475": [{"E": "N", "L": "6"}], "3480": [{"E": "N", "L": "6"}],
           "3481": [{"E": "N", "L": "6"}], "3482": [{"E": "N", "L": "6"}],
           "3483": [{"E": "N", "L": "6"}], "3484": [{"E": "N", "L": "6"}],
           "3485": [{"E": "N", "L": "6"}], "3490": [{"E": "N", "L": "6"}],
           "3491": [{"E": "N", "L": "6"}], "3492": [{"E": "N", "L": "6"}],
           "3493": [{"E": "N", "L": "6"}], "3494": [{"E": "N", "L": "6"}],
           "3495": [{"E": "N", "L": "6"}], "3500": [{"E": "N", "L": "6"}],
           "3501": [{"E": "N", "L": "6"}], "3502": [{"E": "N", "L": "6"}],
           "3503": [{"E": "N", "L": "6"}], "3504": [{"E": "N", "L": "6"}],
           "3505": [{"E": "N", "L": "6"}], "3510": [{"E": "N", "L": "6"}],
           "3511": [{"E": "N", "L": "6"}], "3512": [{"E": "N", "L": "6"}],
           "3513": [{"E": "N", "L": "6"}], "3514": [{"E": "N", "L": "6"}],
           "3515": [{"E": "N", "L": "6"}], "3520": [{"E": "N", "L": "6"}],
           "3521": [{"E": "N", "L": "6"}], "3522": [{"E": "N", "L": "6"}],
           "3523": [{"E": "N", "L": "6"}], "3524": [{"E": "N", "L": "6"}],
           "3525": [{"E": "N", "L": "6"}], "3530": [{"E": "N", "L": "6"}],
           "3531": [{"E": "N", "L": "6"}], "3532": [{"E": "N", "L": "6"}],
           "3533": [{"E": "N", "L": "6"}], "3534": [{"E": "N", "L": "6"}],
           "3535": [{"E": "N", "L": "6"}], "3540": [{"E": "N", "L": "6"}],
           "3541": [{"E": "N", "L": "6"}], "3542": [{"E": "N", "L": "6"}],
           "3543": [{"E": "N", "L": "6"}], "3544": [{"E": "N", "L": "6"}],
           "3545": [{"E": "N", "L": "6"}], "3550": [{"E": "N", "L": "6"}],
           "3551": [{"E": "N", "L": "6"}], "3552": [{"E": "N", "L": "6"}],
           "3553": [{"E": "N", "L": "6"}], "3554": [{"E": "N", "L": "6"}],
           "3555": [{"E": "N", "L": "6"}], "3560": [{"E": "N", "L": "6"}],
           "3561": [{"E": "N", "L": "6"}], "3562": [{"E": "N", "L": "6"}],
           "3563": [{"E": "N", "L": "6"}], "3564": [{"E": "N", "L": "6"}],
           "3565": [{"E": "N", "L": "6"}], "3570": [{"E": "N", "L": "6"}],
           "3571": [{"E": "N", "L": "6"}], "3572": [{"E": "N", "L": "6"}],
           "3573": [{"E": "N", "L": "6"}], "3574": [{"E": "N", "L": "6"}],
           "3575": [{"E": "N", "L": "6"}], "3600": [{"E": "N", "L": "6"}],
           "3601": [{"E": "N", "L": "6"}], "3602": [{"E": "N", "L": "6"}],
           "3603": [{"E": "N", "L": "6"}], "3604": [{"E": "N", "L": "6"}],
           "3605": [{"E": "N", "L": "6"}], "3610": [{"E": "N", "L": "6"}],
           "3611": [{"E": "N", "L": "6"}], "3612": [{"E": "N", "L": "6"}],
           "3613": [{"E": "N", "L": "6"}], "3614": [{"E": "N", "L": "6"}],
           "3615": [{"E": "N", "L": "6"}], "3620": [{"E": "N", "L": "6"}],
           "3621": [{"E": "N", "L": "6"}], "3622": [{"E": "N", "L": "6"}],
           "3623": [{"E": "N", "L": "6"}], "3624": [{"E": "N", "L": "6"}],
           "3625": [{"E": "N", "L": "6"}], "3630": [{"E": "N", "L": "6"}],
           "3631": [{"E": "N", "L": "6"}], "3632": [{"E": "N", "L": "6"}],
           "3633": [{"E": "N", "L": "6"}], "3634": [{"E": "N", "L": "6"}],
           "3635": [{"E": "N", "L": "6"}], "3640": [{"E": "N", "L": "6"}],
           "3641": [{"E": "N", "L": "6"}], "3642": [{"E": "N", "L": "6"}],
           "3643": [{"E": "N", "L": "6"}], "3644": [{"E": "N", "L": "6"}],
           "3645": [{"E": "N", "L": "6"}], "3650": [{"E": "N", "L": "6"}],
           "3651": [{"E": "N", "L": "6"}], "3652": [{"E": "N", "L": "6"}],
           "3653": [{"E": "N", "L": "6"}], "3654": [{"E": "N", "L": "6"}],
           "3655": [{"E": "N", "L": "6"}], "3660": [{"E": "N", "L": "6"}],
           "3661": [{"E": "N", "L": "6"}], "3662": [{"E": "N", "L": "6"}],
           "3663": [{"E": "N", "L": "6"}], "3664": [{"E": "N", "L": "6"}],
           "3665": [{"E": "N", "L": "6"}], "3670": [{"E": "N", "L": "6"}],
           "3671": [{"E": "N", "L": "6"}], "3672": [{"E": "N", "L": "6"}],
           "3673": [{"E": "N", "L": "6"}], "3674": [{"E": "N", "L": "6"}],
           "3675": [{"E": "N", "L": "6"}], "3680": [{"E": "N", "L": "6"}],
           "3681": [{"E": "N", "L": "6"}], "3682": [{"E": "N", "L": "6"}],
           "3683": [{"E": "N", "L": "6"}], "3684": [{"E": "N", "L": "6"}],
           "3685": [{"E": "N", "L": "6"}], "3690": [{"E": "N", "L": "6"}],
           "3691": [{"E": "N", "L": "6"}], "3692": [{"E": "N", "L": "6"}],
           "3693": [{"E": "N", "L": "6"}], "3694": [{"E": "N", "L": "6"}],
           "3695": [{"E": "N", "L": "6"}], "37": [{"E": "N", "M": "8"}],
           "3900": [{"E": "N", "M": "15"}], "3901": [{"E": "N", "M": "15"}],
           "3902": [{"E": "N", "M": "15"}], "3903": [{"E": "N", "M": "15"}],
           "3904": [{"E": "N", "M": "15"}], "3905": [{"E": "N", "M": "15"}],
           "3906": [{"E": "N", "M": "15"}], "3907": [{"E": "N", "M": "15"}],
           "3908": [{"E": "N", "M": "15"}], "3909": [{"E": "N", "M": "15"}],
           "3910": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3911": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3912": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3913": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3914": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3915": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3916": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3917": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3918": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3919": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3920": [{"E": "N", "M": "15"}], "3921": [{"E": "N", "M": "15"}],
           "3922": [{"E": "N", "M": "15"}], "3923": [{"E": "N", "M": "15"}],
           "3924": [{"E": "N", "M": "15"}], "3925": [{"E": "N", "M": "15"}],
           "3926": [{"E": "N", "M": "15"}], "3927": [{"E": "N", "M": "15"}],
           "3928": [{"E": "N", "M": "15"}], "3929": [{"E": "N", "M": "15"}],
           "3930": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3931": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3932": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3933": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3934": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3935": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3936": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3937": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3938": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3939": [{"E": "N", "L": "3"}, {"E": "N", "M": "15"}],
           "3940": [{"E": "N", "L": "4"}], "3941": [{"E": "N", "L": "4"}],
           "3942": [{"E": "N", "L": "4"}], "3943": [{"E": "N", "L": "4"}],
           "400": [{"E": "X", "M": "30"}], "401": [{"E": "X", "M": "30"}],
           "402": [{"E": "N", "L": "17"}], "403": [{"E": "X", "M": "30"}],
           "410": [{"E": "N", "L": "13"}], "411": [{"E": "N", "L": "13"}],
           "412": [{"E": "N", "L": "13"}], "413": [{"E": "N", "L": "13"}],
           "414": [{"E": "N", "L": "13"}], "415": [{"E": "N", "L": "13"}],
           "416": [{"E": "N", "L": "13"}], "420": [{"E": "X", "M": "20"}],
           "421": [{"E": "N", "L": "3"}, {"E": "X", "M": "9"}],
           "422": [{"E": "N", "L": "3"}],
           "423": [{"E": "N", "L": "3"}, {"E": "N", "M": "12"}],
           "424": [{"E": "N", "L": "3"}],
           "425": [{"E": "N", "L": "3"}, {"E": "N", "M": "12"}],
           "426": [{"E": "N", "L": "3"}], "427": [{"E": "X", "M": "3"}],
           "7001": [{"E": "N", "L": "13"}], "7002": [{"E": "X", "M": "30"}],
           "7003": [{"E": "N", "L": "10"}], "7004": [{"E": "N", "M": "4"}],
           "7005": [{"E": "X", "M": "12"}], "7006": [{"E": "N", "L": "6"}],
           "7007": [{"E": "N", "L": "6"}, {"E": "N", "M": "6"}],
           "7008": [{"E": "X", "M": "3"}], "7009": [{"E": "X", "M": "10"}],
           "7010": [{"E": "X", "M": "2"}], "7020": [{"E": "X", "M": "20"}],
           "7021": [{"E": "X", "M": "20"}], "7022": [{"E": "X", "M": "20"}],
           "7023": [{"E": "X", "M": "30"}],
           "7030": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7031": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7032": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7033": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7034": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7035": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7036": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7037": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7038": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "7039": [{"E": "N", "L": "3"}, {"E": "X", "M": "27"}],
           "710": [{"E": "X", "M": "20"}], "711": [{"E": "X", "M": "20"}],
           "712": [{"E": "X", "M": "20"}], "713": [{"E": "X", "M": "20"}],
           "714": [{"E": "X", "M": "20"}], "7230": [{"E": "X", "M": "30"}],
           "7231": [{"E": "X", "M": "30"}], "7232": [{"E": "X", "M": "30"}],
           "7233": [{"E": "X", "M": "30"}], "7234": [{"E": "X", "M": "30"}],
           "7235": [{"E": "X", "M": "30"}], "7236": [{"E": "X", "M": "30"}],
           "7237": [{"E": "X", "M": "30"}], "7238": [{"E": "X", "M": "30"}],
           "7239": [{"E": "X", "M": "30"}], "8001": [{"E": "N", "L": "14"}],
           "8002": [{"E": "X", "M": "20"}],
           "8003": [{"E": "N", "L": "14"}, {"E": "X", "M": "16"}],
           "8004": [{"E": "X", "M": "30"}], "8005": [{"E": "N", "L": "6"}],
           "8006": [{"E": "N", "L": "18"}], "8007": [{"E": "X", "M": "24"}],
           "8008": [{"E": "N", "L": "8"}, {"E": "N", "M": "4"}],
           "8009": [{"E": "X", "M": "50"}], "8010": [{"E": "X", "M": "30"}],
           "8011": [{"E": "N", "M": "12"}], "8012": [{"E": "X", "M": "20"}],
           "8013": [{"E": "X", "M": "30"}], "8017": [{"E": "N", "L": "18"}],
           "8018": [{"E": "N", "L": "18"}], "8019": [{"E": "N", "M": "10"}],
           "8020": [{"E": "X", "M": "25"}], "8026": [{"E": "N", "L": "18"}],
           "8110": [{"E": "X", "M": "70"}], "8111": [{"E": "N", "L": "4"}],
           "8112": [{"E": "X", "M": "70"}], "8200": [{"E": "X", "M": "70"}],
           "90": [{"E": "X", "M": "30"}], "91": [{"E": "X", "M": "90"}],
           "92": [{"E": "X", "M": "90"}], "93": [{"E": "X", "M": "90"}],
           "94": [{"E": "X", "M": "90"}], "95": [{"E": "X", "M": "90"}],
           "96": [{"E": "X", "M": "90"}], "97": [{"E": "X", "M": "90"}],
           "98": [{"E": "X", "M": "90"}], "99": [{"E": "X", "M": "90"}]
           }