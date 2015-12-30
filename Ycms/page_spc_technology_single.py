{% extends "cms/base.html" %}
{% block main %}
  {% load staticfiles %}
		<div id="main" class="toplvl-box"> 
			<div class="cate-kj-content"> 
				<div class="content-lft">
					<div class="head">
						<div class="head-content">
							<span class="sec" id='gyjj' mark="gyjj">工艺简介</span>
							<span class="sec" mark="dtys">动态演示</span>
							<span class="sec" mark="sdkj">四大科技</span>
							<span class="sec" mark="qdtd">七大特点</span>
						</div>
						<div class="foot">
							<span class="up scroll-nrw">&nbsp;</span>
							<span class="down scroll-nrw">&nbsp;</span>
						</div>
						<div class="clr"></div>
					</div>
					<div class="main">
						<div class="scroll-content content">
                          
						</div>
						<div class="content-rgt"></div>
					</div>
					<div class="kj-thumb">
                      <a href="/cms/?m=4a&aid=6"><div id='4a'></div></a>
						<a href="/cms/?m=eeq&aid=7"><div id='eeq'></div></a>
						<a href="/cms/?m=upc&aid=8"><div id='upc'></div></a>
						<a href="/cms/?m=t-plus&aid=9"><div id='rk'></div></a>
					</div>
				</div>
			</div>
		</div>
	<div id="bg-wrapper">
			<img id="bg-all" style="display:none;width:100%;" src="{% static 'cms/default/images/bgbig/a12.jpg' %}"  />
		</div>
<script>

var data = {'gyjj':' <span>在乔治白技术研发中心，新材料的应用与功能性产品的开发取得一次次突破，不断给市场带来惊喜。但我们从不满足于过去的成就，我们不断对技术和解决方案进行创新，以满足现代商务人群对不同气候、环境的需求。 乔治白率先将新雪丽保温材料引入衬衫领域，并应用人体工程学令纤薄隔热层与衬衫完美结合，使衬衫具备优越的保暖性，且顺直服帖。此外，为应对不同气候条件的需求，在吸湿、排汗的基础上，桑蚕丝、竹纤维等保暖材料也将被应用。 与此同时，我们充分理解在严寒的气候，仅仅保暖是远不够的。乔治白成衣纳米抗污技术，将纳米材料直接与纤维发生交联反应，在纤维表面上形成一层纳米级厚度的保护膜，使得织物表面呈现纳米级几何形状互补的界面结构，每个微孔的大小大约只有一滴水的万分之一，这就意味着，在织物表面有效形成“荷叶效应”，对各种水渍、油渍、干污形成天然屏障，有效抵制污渍。不仅如此，基于面料特殊后整理，丝毫不损伤织物的呼吸性能，微孔的大小是水汽分子的上百倍，汗液能透过微孔轻易地蒸发掉，从而保证您从内到外都干爽舒适，良好的透气性是保证您舒适的一个重要因素。 每一款4A热保护功能性衬衫整个生产过程采用的是生态环保工艺，全程不产生污染物排放，无残留，天然环保。4A热保护功能性衬衫持久保暖、抗污、透气，并自始至终保持其出色的性能。 集合了原材料和面料特殊后整理两个领域的科研成果，是继EEQ记忆衬衫后的又一技术革新。 </span>',
  'dtys':'<span> <div style="margin:10px 0px 0px 60px;padding:0px" class="player video-box"> <embed src="/static/pub/ckplayer/ckplayer.swf" flashvars="f=/static/cms/default/images/4a.flv&p=0&i=/static/cms/default/images/video-index-thumb.png" quality="high" width="428" height="229" align="middle" allowScriptAccess="always" allowFullscreen="true" type="application/x-shockwave-flash"></embed> </div> </span>',
            'sdkj':'<span> <strong>保暖(Attach-Thinsulate )</strong><br/> 加入纤薄“新雪丽”隔热层，隔绝空气与热气的对流，反射人体的红外辐射热，锁住热能。<br/> <strong> 抗污(Anti-fouling) </strong><br/> 纤维表面形成“荷叶效应”，阻隔细微漂浮物与颗粒吸附，防止液态物渗透扩散。<br/> <strong> 透气(All-breathability)<br/> </strong> 面料经特殊后整理，不损伤织物呼吸性能，汗液透过微孔快速蒸发，穿着干爽舒适。<br/> <strong> 绿色(Always-ecological)<br/> </strong> 全程采用生态环保工艺，天然环保。<br/> </span>',
            'qdtd':'<span> 1. 持久抗污，最难打理的领窝同样时刻享受清爽；<br/> 2.  热能共同作用于身体各部位，让您享受温暖舒适；<br/> 3.  传输热量并维持平衡，保护您不受恶劣天气困扰；<br/> 4.  收腰贴体，更显身材；<br/> 5.  袖山结构和新工艺的完美结合，确保活动自如；<br/> 6.  下摆轻柔顺直，适应收放喜好；<br/> 7.  加强抗污的同时，锁住内部温度。<br/> </span>' }
$(function(){
    chgCtnt($('#gyjj'));
    $('.sec').on('click', function(){
        chgCtnt($(this));
      })
    function chgCtnt(obj){
        var dmark = obj.attr('mark');
        var str  = data[dmark];
        $('.sec').css({'color':'#666','background':''});
        obj.css({'color':'#fff','background':'#009966'});
        $('.scroll-content').html('');
        $('.scroll-content').html(str);
    }
    })
</script>
  {% endblock %}
