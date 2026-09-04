#!/usr/bin/env python3
"""
生成8月份AI月报HTML
基于7月份模板，更新内容和图片
"""

import base64
import os
import re
from pathlib import Path

# 路径配置
BASE_DIR = Path("/Users/aaa/Desktop/客服系统/AI工作/AI月报")
M7_HTML = BASE_DIR / "2026-M7" / "客服中心AI月报-M7.html"
M8_DIR = BASE_DIR / "2026-M8"
M8_IMAGES = M8_DIR / "项目图片"
OUTPUT_HTML = M8_DIR / "客服中心AI月报-M8.html"

# 8月份物料内容
M8_CONTENT = {
    "title": "客服中心AI月报 · 2026年8月",
    "stats": {
        "launched": 6,      # 已上线项目数
        "in_progress": 4,   # 进行中项目数
        "ai_ratio": "76%"   # AI服务占比
    },
    "launched_projects": [
        {
            "name": "售前智能客服定向入口优化",
            "tag": "定向推送 · 智能问答",
            "desc": "新增23个定向入口并推送定向猜你想问，同时售前客服报表支持端平品、场景及产品的筛选，提升售前客服精准度和用户体验",
            "image": "售前客服.png"
        },
        {
            "name": "AI搜接入客服",
            "tag": "全量上线 · 前端交互",
            "desc": "对接AI搜的前端交互已上线，为用户提供更智能的搜索和客服体验",
            "image": "ai搜.jpg"
        },
        {
            "name": "纳逗pro接入专属客服",
            "tag": "专属服务 · 智能接入",
            "desc": "纳逗pro成功接入专属客服，为用户提供更个性化、专业的客服服务体验",
            "image": "纳逗pro.jpg"
        },
        {
            "name": "坐席助手服务质量提升",
            "tag": "服务融合 · 智能答复",
            "desc": "由原先服务用语与业务分析分别独立处理，调整为服务用语与业务分析融合后统一生成答复并发送，大幅提升坐席助手服务效率和质量",
            "image": "坐席助手.png"
        }
    ],
    "ongoing_projects": [
        {
            "name": "智能在线前端交互灰度上线",
            "tag": "灰度发布 · 图片识别",
            "desc": "智能在线前端交互灰度上线，支持图片识别功能，为用户提供更丰富的交互体验",
            "image": "智能在线前端交互改版.png"
        },
        {
            "name": "国际站对接生成式智能客服",
            "tag": "海外客诉 · 实时处理",
            "desc": "海外客诉处理链路升级，将迟滞性客诉升级为实时业务，端内帮助反馈、客服邮箱、Facebook私信三类海外客诉渠道统一接入生成式智能客服实现实时处理，预期落地后整体平均处理周期由15.5h缩短到4.4h"
        },
        {
            "name": "智能在线猜你想问推送策略优化",
            "tag": "策略升级 · 精准推送",
            "desc": "在原有特征行为上新增2层架构：根据用户重点行为强特征匹配专属问题（如播放失败、账号封停、还款失败等）；根据入口特征进行专属问题推送（如小芽贷、微短剧等定向入口推送）"
        },
        {
            "name": "天工项目",
            "tag": "知识体系 · 技能重构",
            "desc": "天工项目是客服中心以'客服技能(Skill)'为最小单元的业务流程与知识体系重构工程。把'怎么处理一类真实用户问题'的能力沉淀为标准Skill，而不是按产品分类、工单分类或单点操作步骤来组织"
        }
    ],
    "tech_exploration": {
        "name": "对话质量提升专项",
        "tag": "AI分析驱动 · 可观测性",
        "desc": "以AI分析驱动对话质量提升，构建可观测性的质量评分体系，实现发现问题、改进问题、效果评估等多环节闭环管理，持续提升AI答复质量和服务水平",
        "image": "智能客服对话质量提升专项.png"
    }
}

def image_to_base64(image_path: Path) -> str:
    """将图片转换为base64编码"""
    if not image_path.exists():
        print(f"警告: 图片不存在 {image_path}")
        return ""

    with open(image_path, "rb") as f:
        image_data = f.read()

    # 根据文件扩展名确定MIME类型
    suffix = image_path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif"
    }
    mime_type = mime_types.get(suffix, "image/png")

    base64_data = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"

def build_single_project_card(project: dict) -> str:
    """构建单个项目卡片（上下结构：文字在上，图片在下）"""
    image_html = ""
    if "image" in project and project["image"]:
        image_path = M8_IMAGES / project["image"]
        base64_src = image_to_base64(image_path)
        if base64_src:
            # 根据项目名称设置不同的图片尺寸
            if project["name"] == "售前智能客服定向入口优化":
                # 售前客服：放大，左右贴合边框
                image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{project['name']}" width="100%" style="display:block; width:100%; height:auto; border:1px solid #e8e8e8;" />
        </td></tr>'''
            elif project["name"] == "坐席助手服务质量提升":
                # 坐席助手：放大，左右贴合边框
                image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{project['name']}" width="100%" style="display:block; width:100%; height:auto; border:1px solid #e8e8e8;" />
        </td></tr>'''
            elif project["name"] == "智能在线前端交互灰度上线":
                # 智能客服前端交互改版：缩小
                image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{project['name']}" width="500" style="display:block; max-width:500px; width:100%; height:auto; border:1px solid #e8e8e8;" />
        </td></tr>'''
            else:
                # 其他项目：默认尺寸
                image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{project['name']}" width="805" style="display:block; max-width:805px; width:100%; height:auto; border:1px solid #e8e8e8;" />
        </td></tr>'''

    return f'''
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:20px;">
    <tr><td bgcolor="#f8f9fa" style="background-color:#f8f9fa; padding:20px; border:1px solid #e8e8e8;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr><td style="font-family:Arial, sans-serif; font-size:15px; font-weight:bold; color:#1a1a2e; padding-bottom:2px;">{project['name']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:11px; color:#999999; padding-bottom:12px;">{project['tag']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:13px; color:#666666; line-height:1.8; padding-bottom:14px;">{project['desc']}</td></tr>
        {image_html}
        </table>
    </td></tr>
    </table>'''

def build_project_html(project: dict, index: int, is_launched: bool = True) -> str:
    """构建单个项目的HTML（用于普通上下结构项目）"""
    return build_single_project_card(project)

def build_side_by_side_projects_html(project1: dict, project2: dict) -> str:
    """构建两个项目并排显示的HTML"""
    # 为每个项目构建卡片内容（不包含最外层table）
    def build_card_content(project):
        image_html = ""
        if "image" in project and project["image"]:
            image_path = M8_IMAGES / project["image"]
            base64_src = image_to_base64(image_path)
            if base64_src:
                # AI搜接入客服和纳逗pro：缩小图片
                image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{project['name']}" width="300" style="display:block; max-width:300px; width:100%; height:auto; border:1px solid #e8e8e8;" />
        </td></tr>'''
        return image_html

    return f'''
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:20px;">
    <tr>
        <td width="49%" valign="top" style="padding-right:10px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr><td bgcolor="#f8f9fa" style="background-color:#f8f9fa; padding:20px; border:1px solid #e8e8e8;">
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr><td style="font-family:Arial, sans-serif; font-size:15px; font-weight:bold; color:#1a1a2e; padding-bottom:2px;">{project1['name']}</td></tr>
                <tr><td style="font-family:Arial, sans-serif; font-size:11px; color:#999999; padding-bottom:12px;">{project1['tag']}</td></tr>
                <tr><td style="font-family:Arial, sans-serif; font-size:13px; color:#666666; line-height:1.8; padding-bottom:14px;">{project1['desc']}</td></tr>
                {build_card_content(project1)}
                </table>
            </td></tr>
            </table>
        </td>
        <td width="2%">&nbsp;</td>
        <td width="49%" valign="top" style="padding-left:10px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr><td bgcolor="#f8f9fa" style="background-color:#f8f9fa; padding:20px; border:1px solid #e8e8e8;">
                <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr><td style="font-family:Arial, sans-serif; font-size:15px; font-weight:bold; color:#1a1a2e; padding-bottom:2px;">{project2['name']}</td></tr>
                <tr><td style="font-family:Arial, sans-serif; font-size:11px; color:#999999; padding-bottom:12px;">{project2['tag']}</td></tr>
                <tr><td style="font-family:Arial, sans-serif; font-size:13px; color:#666666; line-height:1.8; padding-bottom:14px;">{project2['desc']}</td></tr>
                {build_card_content(project2)}
                </table>
            </td></tr>
            </table>
        </td>
    </tr>
    </table>'''

def build_m8_html() -> str:
    """构建完整的8月份HTML"""
    # 读取7月份模板
    with open(M7_HTML, "r", encoding="utf-8") as f:
        template = f.read()

    # 更新标题和月份
    html = template.replace("客服中心AI月报 · 2026年7月", M8_CONTENT["title"])
    html = html.replace("2026年7月", "2026年8月")

    # 更新关键成果数据
    html = re.sub(
        r'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#00c853; line-height:1;">\d+</td>',
        f'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#00c853; line-height:1;">{M8_CONTENT["stats"]["launched"]}</td>',
        html, count=1
    )
    html = re.sub(
        r'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#ff9800; line-height:1;">\d+</td>',
        f'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#ff9800; line-height:1;">{M8_CONTENT["stats"]["in_progress"]}</td>',
        html, count=1
    )
    html = re.sub(
        r'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#2196f3; line-height:1;">\d+%</td>',
        f'<td align="center" style="font-family:Arial, sans-serif; font-size:40px; font-weight:bold; color:#2196f3; line-height:1;">{M8_CONTENT["stats"]["ai_ratio"]}</td>',
        html, count=1
    )

    # 构建已上线项目HTML
    launched_html = ""
    i = 0
    while i < len(M8_CONTENT["launched_projects"]):
        project = M8_CONTENT["launched_projects"][i]
        if project["name"] == "AI搜接入客服" and i + 1 < len(M8_CONTENT["launched_projects"]):
            next_project = M8_CONTENT["launched_projects"][i + 1]
            if next_project["name"] == "纳逗pro接入专属客服":
                launched_html += build_side_by_side_projects_html(project, next_project)
                i += 2
                continue
        launched_html += build_project_html(project, i, is_launched=True)
        i += 1

    # 构建持续推进项目HTML
    ongoing_html = ""
    for i, project in enumerate(M8_CONTENT["ongoing_projects"]):
        ongoing_html += build_project_html(project, i, is_launched=False)

    # 替换已上线项目内容 - 使用更简单的方法
    # 找到已上线重点项目部分的开始和结束
    launched_section_start = html.find('<!-- ===== LAUNCHED PROJECTS ===== -->')
    launched_section_end = html.find('<!-- ===== ONGOING PROJECTS ===== -->')

    if launched_section_start != -1 and launched_section_end != -1:
        # 找到标题table的结束位置
        # 标题table结构：<table ...><tr><td width="4" bgcolor="#00c853"></td><td>已上线重点项目</td></tr></table>
        title_table_start = html.find('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">', launched_section_start + len('<!-- ===== LAUNCHED PROJECTS ===== -->'))
        if title_table_start != -1:
            # 找到标题table的结束
            title_table_end = html.find('</table>', title_table_start) + len('</table>')
            # 提取标题部分（从注释到标题table结束）
            section_header = html[launched_section_start:title_table_end]

            # 构建新的已上线项目部分
            new_launched_section = section_header + '\n\n' + launched_html + '\n    </td></tr>\n</table>\n'

            # 替换从标题table结束到ONGOING PROJECTS开始的内容
            html = html[:launched_section_start] + new_launched_section + html[launched_section_end:]

    # 替换持续推进项目内容
    ongoing_section_start = html.find('<!-- ===== ONGOING PROJECTS ===== -->')
    ongoing_section_end = html.find('<!-- ===== TECH EXPLORATION ===== -->')

    if ongoing_section_start != -1 and ongoing_section_end != -1:
        # 找到标题table的结束位置
        # 标题table结构：<table ...><tr><td width="4" bgcolor="#ff9800"></td><td>持续推进的项目</td></tr></table>
        title_table_start = html.find('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">', ongoing_section_start + len('<!-- ===== ONGOING PROJECTS ===== -->'))
        if title_table_start != -1:
            # 找到标题table的结束
            title_table_end = html.find('</table>', title_table_start) + len('</table>')
            # 提取标题部分（从注释到标题table结束）
            section_header = html[ongoing_section_start:title_table_end]

            # 构建新的持续推进项目部分
            new_ongoing_section = section_header + '\n\n' + ongoing_html + '\n    </td></tr>\n</table>\n'

            # 替换从标题table结束到TECH EXPLORATION开始的内容
            html = html[:ongoing_section_start] + new_ongoing_section + html[ongoing_section_end:]

    # 更新技术探索部分
    tech_section_start = html.find('<!-- ===== TECH EXPLORATION ===== -->')
    tech_section_end = html.find('<!-- ===== FOOTER ===== -->')

    if tech_section_start != -1 and tech_section_end != -1:
        # 找到标题table的结束位置
        title_table_start = html.find('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">', tech_section_start + len('<!-- ===== TECH EXPLORATION ===== -->'))
        if title_table_start != -1:
            title_table_end = html.find('</table>', title_table_start) + len('</table>')
            section_header = html[tech_section_start:title_table_end]

            # 构建技术探索项目卡片
            tech = M8_CONTENT["tech_exploration"]
            image_html = ""
            if "image" in tech and tech["image"]:
                image_path = M8_IMAGES / tech["image"]
                base64_src = image_to_base64(image_path)
                if base64_src:
                    image_html = f'''
        <tr><td style="padding-top:14px;">
            <img src="{base64_src}" alt="{tech['name']}" width="805" style="display:block; max-width:805px; width:100%; height:auto; border:1px solid #90caf9;" />
        </td></tr>'''

            tech_card = f'''
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:20px;">
    <tr><td bgcolor="#e3f2fd" style="background-color:#e3f2fd; padding:20px; border:1px solid #90caf9;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr><td style="font-family:Arial, sans-serif; font-size:15px; font-weight:bold; color:#1565c0; padding-bottom:2px;">{tech['name']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:11px; color:#64b5f6; padding-bottom:12px;">{tech['tag']}</td></tr>
        <tr><td style="font-family:Arial, sans-serif; font-size:13px; color:#666666; line-height:1.8; padding-bottom:14px;">{tech['desc']}</td></tr>
        {image_html}
        </table>
    </td></tr>
    </table>'''

            new_tech_section = section_header + '\n\n' + tech_card + '\n    </td></tr>\n</table>\n'
            html = html[:tech_section_start] + new_tech_section + html[tech_section_end:]

    return html

def main():
    """主函数"""
    print("开始生成8月份AI月报...")

    # 检查模板文件是否存在
    if not M7_HTML.exists():
        print(f"错误: 找不到7月份模板文件 {M7_HTML}")
        return

    # 检查图片目录是否存在
    if not M8_IMAGES.exists():
        print(f"错误: 找不到图片目录 {M8_IMAGES}")
        return

    # 生成HTML
    html = build_m8_html()

    # 保存文件
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 8月份AI月报已生成: {OUTPUT_HTML}")
    print(f"📊 关键成果: {M8_CONTENT['stats']['launched']}项已上线, {M8_CONTENT['stats']['in_progress']}项进行中, AI服务占比{M8_CONTENT['stats']['ai_ratio']}")

if __name__ == "__main__":
    main()
