from random import randint
songs = ["[spuh<300,19>kiy<300,19>skeh<300,18>riy<300,18>skeh<300,11>lleh<175,14>tih<200,11>ns] [seh<300,11>nd][shih<100,19>ver<500,19>sdaw<300,18>nyur<300,18>spay<300,11>n] [shriy<300,19>kiy<300,19>ng][skow<300,18>swih<300,18>ll][shah<300,11>kyur<300,14>sow<300,11>ll] [siy<300,14>llyur<300,16>duh<300,13>mtuh<300,14>nay<300,11>t]",
         "[dah<600,20>][dah<600,20>][dah<600,20>][dah<500,16>][dah<130,23>][dah<600,20>][dah<500,16>][dah<130,23>][dah<600,20>] [dah<600,27>][dah<600,27>][dah<600,27>][dah<500,28>][dah<130,23>][dah<600,19>][dah<500,15>][dah<130,23>][dah<600,20>] [dah<600,32>][dah<600,20>][dah<600,32>][dah<600,31>][dah<100,30>][dah<100,29>][dah<100,28>][dah<300,29>] [dah<150,18>][dah<600,28>][dah<600,27>][dah<100,26>][dah<100,25>][dah<100,24>][dah<100,26>] [dah<150,15>][dah<600,20>][dah<600,16>][dah<150,23>][dah<600,20>][dah<600,20>][dah<150,23>][dah<600,27>] [dah<600,32>][dah<600,20>][dah<600,32>][dah<600,31>][dah<100,30>][dah<100,29>][dah<100,28>][dah<300,29>] [dah<150,18>][dah<600,28>][dah<600,27>][dah<100,26>][dah<100,25>][dah<100,24>][dah<100,26>] [dah<150,15>][dah<600,20>][dah<600,16>][dah<150,23>][dah<600,20>][dah<600,16>][dah<150,23>][dah<600,20>]",
         "[jhah<800,13>nmae<800,15>deh<800,17>]n[_<800,17>][jhah<800,17>nmae<800,18>deh<800,20>n] [jhah<400,20>ah<800,25>ah<400,24>ah<400,25>ah<800,20>ah<400,18>ah<800,17>nmae<800,15>deh<800,13>n]",
         "[dah<300,30>][dah<60,30>][dah<200,25>][dah<1000,30>][dah<200,23>][dah<400,25>][dah<700,18>]",
         "[:t 430,500][:t 320,250][:t 350,250][:t 390,500][:t 350,250][:t 330,250][:t 290,500][:t 290,250][:t 350,250][:t 430,500]",
         "[:t 520,250][:t 520,250][:t 460,250][:t 520,500][:t 390,500][:t 390,250][:t 520,250][:t 700,250][:t 660,250][:t 520,500]",
         "[:tone 165,200][:tone 165,400][:tone 165,400][:tone 131,200][:tone 165,400][:tone 196,800][:tone 98,1000]",
         "[_<1,13>]we're[_<1,18>]whalers[_<1,17]on[_<1,18>]the[_<1,20>]moon[_<400,13>]we[_<1,20>]carry[_<1,18>]a[_<1,20>]har[_<1,22>]poon [_<1,22>]but there[_<1,23>]aint no[_<1,15>]whales[_<1,23>]so we[_<1,22>]tell tall[_<1,18>]tales and [_<1,20>]sing our[_<1,18>]whale[_<1,17>]ing[_<1,18>]tune",
         "[_<1,30>]spayyyyyyyyyyyace",
         "[:dial6387657]The birth parents you are trying to call do not love you, please hang up[:t 350,500][:t 1,500][:t 350,500]",
         "Dram[aa<250,21>] matic [hxae<250,26>]coir[hxae<250,28>]na[aa<450,29>][aa<200,26>]with jonh[mae<900,24>deh<1000,26>nn]",
         "[lxao<400,23>lxao<800,28>lxao<600,23>lxao<200,25>lx ao<1600,27>lxao<800,25>lxao<600,23>lxao<200,21>lxa o<1600,23>] [lxao<400,16>][lxao<400,16>][lxao<800,18>][lxao<400,18>][lxao<400,20>][lxao<800,21>][lxao<400,21>][lxao<400,23>] [lxao<800,25>][lxao<400,27>][lxao<400,28>][lxao<800,30>][_<400,23>][lxao<400,23>][lxao<800,32>][lxao<600,30>] [lxao<200,28>][lxao<800,30>][lxao<400,27>][lxao<400,23>][lxao<800,28>][lxao<400,27>][lxao<400,25>][lxao<800,27>] [lxao<400,20>][lxao<400,20>][lxao<800,25>][lxao<400,23>][lxao<400,21>][lxao<800,23>][lxao<400,16>][lxao<400,16>] [lxao<800,28>][lxao<800,27>][lxao<200,25>][lxao<1600,23>]",
         "[nae<99,20>nae<99,20>nae<99,19>nae<99,19>nae<99,18>nae<99,18>nae<99,19>nae<99,19>bae<140,25>ttmae<600,25>nn]",
         "[skuw<200,24>biy<200,24>duw<200,22>biy<200,22>duw<600,20>_<200>weh<200,22>rraa<400,24>rryu<600,17>]",
         "[dah<500,26>dah<180,14>dah<180,21>dah<500,19>dah<180,26>dah<500,21>]",
         ]


def get_song():
    choice = randint(0, 14)
    return songs[choice]